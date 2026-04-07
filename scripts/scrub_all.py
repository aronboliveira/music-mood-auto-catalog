import os
import re


def scrub_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception:
            return

    original_content = content

    replacements = [
        (re.compile(r'mockuser', re.IGNORECASE), "mockuser"),
        (re.compile(r'mockdrive', re.IGNORECASE), "mockdrive"),
        (re.compile(r'FictionalGame', re.IGNORECASE), "FictionalGame"),
        (re.compile(r'FictionalGame', re.IGNORECASE), "FictionalGame"),
        (re.compile(r'FictionalAnime', re.IGNORECASE), "FictionalAnime"),
        (re.compile(r'FictionalAnime', re.IGNORECASE), "FictionalAnime"),
        (re.compile(r'FictionalGame2', re.IGNORECASE), "FictionalGame2"),
        (re.compile(r'FictionalGame2', re.IGNORECASE), "FictionalGame2")
    ]

    for pattern, new in replacements:
        content = pattern.sub(new, content)

    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Scrubbed {filepath}")
        except Exception as e:
            print(f"Could not write to {filepath}: {e}")


def main():
    extensions = ('.py', '.sh', '.txt', '.log', '.md', '.json', '.yml', '.html')

    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.venv' in root:
            continue

        for file in files:
            if file.endswith(extensions):
                filepath = os.path.join(root, file)
                scrub_file(filepath)


if __name__ == '__main__':
    main()
