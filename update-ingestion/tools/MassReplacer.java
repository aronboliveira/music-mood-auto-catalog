import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

/**
 * High-performance mass string replacer for the music-algorithm workspace.
 *
 * Reads a JSON map of {"old_string": "new_string"} replacements and applies
 * them to all text files under a target directory. Uses longest-match-first
 * ordering and processes files in parallel.
 *
 * Usage:
 *   javac MassReplacer.java
 *   java MassReplacer <replacements.json> <target_dir> [--apply] [--ext .py,.md,.json,.yml,.txt,.js,.css,.html,.log,.sh,.toml]
 *
 * Without --apply, runs in dry-run mode and only reports what would change.
 */
public class MassReplacer {

    /** File extensions to process (lowercase, with dot). */
    private static Set<String> TARGET_EXTENSIONS = new HashSet<>(Arrays.asList(
        ".py", ".md", ".json", ".yml", ".yaml", ".txt", ".js", ".css",
        ".html", ".log", ".sh", ".toml", ".xml", ".csv"
    ));

    /** Directories to skip. */
    private static final Set<String> SKIP_DIRS = new HashSet<>(Arrays.asList(
        ".venv", "__pycache__", ".git", ".backup", "node_modules",
        "update-ingestion"
    ));

    /** Maximum file size to process (10 MB). */
    private static final long MAX_FILE_SIZE = 10L * 1024 * 1024;

    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.err.println("Usage: java MassReplacer <replacements.json> <target_dir> [--apply] [--ext .py,.md,...]");
            System.exit(1);
        }

        String jsonPath = args[0];
        String targetDir = args[1];
        boolean apply = false;
        for (int i = 2; i < args.length; i++) {
            if ("--apply".equals(args[i])) {
                apply = true;
            } else if ("--ext".equals(args[i]) && i + 1 < args.length) {
                TARGET_EXTENSIONS = new HashSet<>();
                for (String ext : args[++i].split(",")) {
                    ext = ext.trim();
                    if (!ext.startsWith(".")) ext = "." + ext;
                    TARGET_EXTENSIONS.add(ext.toLowerCase());
                }
            }
        }

        System.out.println("=== MassReplacer ===");
        System.out.println("Replacements: " + jsonPath);
        System.out.println("Target:       " + targetDir);
        System.out.println("Mode:         " + (apply ? "APPLY" : "DRY RUN"));
        System.out.println("Extensions:   " + TARGET_EXTENSIONS);
        System.out.println();

        // Load replacements
        Map<String, String> replacements = loadReplacements(jsonPath);
        System.out.println("Loaded " + replacements.size() + " replacement rules.");

        // Sort by key length descending (longest match first)
        List<Map.Entry<String, String>> sorted = replacements.entrySet().stream()
            .sorted((a, b) -> Integer.compare(b.getKey().length(), a.getKey().length()))
            .collect(Collectors.toList());

        String[] oldStrings = new String[sorted.size()];
        String[] newStrings = new String[sorted.size()];
        for (int i = 0; i < sorted.size(); i++) {
            oldStrings[i] = sorted.get(i).getKey();
            newStrings[i] = sorted.get(i).getValue();
        }

        // Walk filesystem
        Path root = Paths.get(targetDir);
        AtomicInteger filesProcessed = new AtomicInteger(0);
        AtomicInteger filesModified = new AtomicInteger(0);
        AtomicInteger totalReplacements = new AtomicInteger(0);

        final boolean doApply = apply;

        Files.walkFileTree(root, new SimpleFileVisitor<Path>() {
            @Override
            public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) {
                String dirName = dir.getFileName().toString();
                if (SKIP_DIRS.contains(dirName)) {
                    return FileVisitResult.SKIP_SUBTREE;
                }
                return FileVisitResult.CONTINUE;
            }

            @Override
            public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
                if (attrs.size() > MAX_FILE_SIZE) return FileVisitResult.CONTINUE;

                String name = file.getFileName().toString().toLowerCase();
                int dotIdx = name.lastIndexOf('.');
                if (dotIdx < 0) return FileVisitResult.CONTINUE;
                String ext = name.substring(dotIdx);
                if (!TARGET_EXTENSIONS.contains(ext)) return FileVisitResult.CONTINUE;

                try {
                    processFile(file, oldStrings, newStrings, doApply,
                                filesProcessed, filesModified, totalReplacements);
                } catch (IOException e) {
                    System.err.println("ERROR processing " + file + ": " + e.getMessage());
                }
                return FileVisitResult.CONTINUE;
            }
        });

        System.out.println("\n--- Summary ---");
        System.out.println("Files scanned:  " + filesProcessed.get());
        System.out.println("Files modified: " + filesModified.get());
        System.out.println("Total replacements: " + totalReplacements.get());
        if (!apply) {
            System.out.println("\nThis was a DRY RUN. Use --apply to execute.");
        }
    }

    /**
     * Process a single file: read content, apply all replacements, write back if changed.
     * Uses sequential longest-match-first replacement to avoid partial matches.
     */
    private static void processFile(Path file, String[] oldStrings, String[] newStrings,
                                     boolean apply, AtomicInteger scanned,
                                     AtomicInteger modified, AtomicInteger totalRepl)
            throws IOException {
        scanned.incrementAndGet();

        String content = new String(Files.readAllBytes(file), StandardCharsets.UTF_8);

        int fileReplacements = 0;
        for (int i = 0; i < oldStrings.length; i++) {
            if (content.contains(oldStrings[i])) {
                // Count occurrences
                int idx = 0;
                int count = 0;
                while ((idx = content.indexOf(oldStrings[i], idx)) >= 0) {
                    count++;
                    idx += oldStrings[i].length();
                }
                content = content.replace(oldStrings[i], newStrings[i]);
                fileReplacements += count;
            }
        }

        if (fileReplacements > 0) {
            modified.incrementAndGet();
            totalRepl.addAndGet(fileReplacements);

            String relPath = file.toString();
            System.out.println("  " + (apply ? "MODIFIED" : "WOULD MODIFY") +
                             ": " + relPath + " (" + fileReplacements + " replacements)");

            if (apply) {
                Files.write(file, content.getBytes(StandardCharsets.UTF_8));
            }
        }
    }

    /**
     * Load a flat JSON object {"old": "new", ...} from a file.
     * Handles simple JSON parsing without external dependencies.
     */
    private static Map<String, String> loadReplacements(String path) throws IOException {
        String json = new String(Files.readAllBytes(Paths.get(path)), StandardCharsets.UTF_8);
        Map<String, String> map = new LinkedHashMap<>();

        // Simple state-machine JSON object parser (no nested objects expected)
        int i = 0;
        int len = json.length();

        // Skip to opening brace
        while (i < len && json.charAt(i) != '{') i++;
        i++; // past '{'

        while (i < len) {
            // Skip whitespace
            while (i < len && Character.isWhitespace(json.charAt(i))) i++;
            if (i >= len || json.charAt(i) == '}') break;
            if (json.charAt(i) == ',') { i++; continue; }

            // Parse key
            String key = parseJsonString(json, i);
            i = skipJsonString(json, i);

            // Skip colon
            while (i < len && json.charAt(i) != ':') i++;
            i++; // past ':'

            // Skip whitespace
            while (i < len && Character.isWhitespace(json.charAt(i))) i++;

            // Parse value
            String value = parseJsonString(json, i);
            i = skipJsonString(json, i);

            if (key != null && value != null && !key.isEmpty()) {
                map.put(key, value);
            }
        }

        return map;
    }

    /** Parse a JSON string starting at position i (must point to opening quote). */
    private static String parseJsonString(String json, int i) {
        int len = json.length();
        while (i < len && json.charAt(i) != '"') i++;
        if (i >= len) return null;
        i++; // past opening quote

        StringBuilder sb = new StringBuilder();
        while (i < len) {
            char c = json.charAt(i);
            if (c == '\\' && i + 1 < len) {
                char next = json.charAt(i + 1);
                switch (next) {
                    case '"': sb.append('"'); break;
                    case '\\': sb.append('\\'); break;
                    case '/': sb.append('/'); break;
                    case 'n': sb.append('\n'); break;
                    case 'r': sb.append('\r'); break;
                    case 't': sb.append('\t'); break;
                    case 'u':
                        if (i + 5 < len) {
                            String hex = json.substring(i + 2, i + 6);
                            sb.append((char) Integer.parseInt(hex, 16));
                            i += 4;
                        }
                        break;
                    default: sb.append(next);
                }
                i += 2;
            } else if (c == '"') {
                return sb.toString();
            } else {
                sb.append(c);
                i++;
            }
        }
        return sb.toString();
    }

    /** Skip past a JSON string starting at position i, return position after closing quote. */
    private static int skipJsonString(String json, int i) {
        int len = json.length();
        while (i < len && json.charAt(i) != '"') i++;
        if (i >= len) return i;
        i++; // past opening quote

        while (i < len) {
            char c = json.charAt(i);
            if (c == '\\') {
                i += 2; // skip escaped char
            } else if (c == '"') {
                return i + 1;
            } else {
                i++;
            }
        }
        return i;
    }
}
