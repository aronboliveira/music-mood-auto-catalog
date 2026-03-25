// moods-checks-app.js — Vue 3 app for Mood Assignments Checker
// Depends on: moods-checks-data.js (ALL_MOODS, MOOD_COLORS, TRACK_MOODS)

const { createApp, ref, computed, onMounted, watch, nextTick } = Vue;

const STORAGE_KEY = "moods-checks-state-v1";

function readStorage() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

createApp({
  setup() {
    // ── Build reactive track list from data ─────────────────────────────
    const trackNames = Object.keys(TRACK_MOODS).sort((a, b) => {
      const strip = (s) => s.replace(/^[\d.\-\s]+/, "").toLowerCase();
      return strip(a).localeCompare(strip(b));
    });

    // Reactive state per track: { reviewed, open, moods: Set }
    const trackState = ref({});

    // Pre-reviewed A-tracks (reviewed up to "Awake FictionalGame Ultimate OST")
    const PRE_REVIEWED =
      typeof REVIEWED_TRACKS !== "undefined"
        ? new Set(REVIEWED_TRACKS)
        : new Set();

    // Initialise from TRACK_MOODS defaults
    trackNames.forEach((name) => {
      trackState.value[name] = {
        reviewed: PRE_REVIEWED.has(name),
        open: false,
        moods: new Set(TRACK_MOODS[name] || []),
      };
    });

    // ── Restore from localStorage ───────────────────────────────────────
    function restoreAll() {
      const saved = readStorage();
      if (!Object.keys(saved).length) return;
      for (const [track, entry] of Object.entries(saved)) {
        if (!trackState.value[track]) continue;
        const ts = trackState.value[track];
        if (typeof entry.reviewed === "boolean") ts.reviewed = entry.reviewed;
        if (typeof entry.open === "boolean") ts.open = entry.open;
        if (Array.isArray(entry.moods)) ts.moods = new Set(entry.moods);
      }
    }

    // ── Save to localStorage (debounced) ────────────────────────────────
    const autosaveMsg = ref("");
    let _saveTimer = null;

    function scheduleSave() {
      if (_saveTimer) clearTimeout(_saveTimer);
      _saveTimer = setTimeout(saveAll, 300);
    }

    function saveAll() {
      const state = {};
      for (const [track, ts] of Object.entries(trackState.value)) {
        state[track] = {
          reviewed: ts.reviewed,
          open: ts.open,
          moods: Array.from(ts.moods),
        };
      }
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        autosaveMsg.value = "auto-saved";
        setTimeout(() => (autosaveMsg.value = ""), 1200);
      } catch (e) {
        console.warn("moods-checks: localStorage write failed", e);
      }
    }

    // ── Search ──────────────────────────────────────────────────────────
    const searchQuery = ref("");
    const filteredTracks = computed(() => {
      const q = searchQuery.value.trim().toLowerCase();
      if (!q) return trackNames;
      return trackNames.filter((n) => n.toLowerCase().includes(q));
    });

    // ── Reviewed stats ──────────────────────────────────────────────────
    const reviewedCount = computed(() => {
      return Object.values(trackState.value).filter((ts) => ts.reviewed).length;
    });
    const reviewedPct = computed(() => {
      return ((reviewedCount.value / trackNames.length) * 100).toFixed(1);
    });

    // ── Toggle mood checkbox ────────────────────────────────────────────
    function toggleMood(track, mood) {
      const ts = trackState.value[track];
      if (ts.moods.has(mood)) ts.moods.delete(mood);
      else ts.moods.add(mood);
      scheduleSave();
    }

    function hasMood(track, mood) {
      return trackState.value[track].moods.has(mood);
    }

    // ── Toggle reviewed ─────────────────────────────────────────────────
    function toggleReviewed(track) {
      trackState.value[track].reviewed = !trackState.value[track].reviewed;
      scheduleSave();
    }

    // ── Toggle open ─────────────────────────────────────────────────────
    function onToggle(track, ev) {
      trackState.value[track].open = ev.target.open;
      scheduleSave();
    }

    // ── Helpers ─────────────────────────────────────────────────────────
    function displayName(filename) {
      return filename.replace(/\.mp3$/i, "").replace(/[-_]/g, " ");
    }

    function moodColor(mood) {
      return MOOD_COLORS[mood] || "#ccc";
    }

    // ── Collect data for export ─────────────────────────────────────────
    function collectData() {
      const result = {};
      for (const [track, ts] of Object.entries(trackState.value)) {
        const moods = Array.from(ts.moods).sort();
        if (moods.length) result[track] = moods;
      }
      return result;
    }

    // ── Export JSON ─────────────────────────────────────────────────────
    const statusMsg = ref("");

    function exportJson() {
      const data = collectData();
      const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: "application/json",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "track-moods.json";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      statusMsg.value = "JSON exported ✓";
      setTimeout(() => (statusMsg.value = ""), 3000);
    }

    // ── Copy YAML to clipboard ──────────────────────────────────────────
    function copyYaml() {
      const data = collectData();
      const lines = Object.entries(data)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([track, moods]) => track + ":\n  - " + moods.join("\n  - "))
        .join("\n");
      navigator.clipboard
        .writeText(lines)
        .then(() => {
          statusMsg.value = "Copied to clipboard ✓";
          setTimeout(() => (statusMsg.value = ""), 3000);
        })
        .catch(() => {
          statusMsg.value = "Clipboard access denied";
        });
    }

    // ── Clear storage ───────────────────────────────────────────────────
    function clearStorage() {
      if (!confirm("Clear all saved progress? This cannot be undone.")) return;
      localStorage.removeItem(STORAGE_KEY);
      statusMsg.value = "Saved state cleared";
      setTimeout(() => (statusMsg.value = ""), 3000);
    }

    // ── Mount lifecycle ─────────────────────────────────────────────────
    onMounted(() => {
      restoreAll();
      // Second pass after a short timeout for safety
      setTimeout(restoreAll, 150);
    });

    return {
      allMoods: ALL_MOODS,
      trackNames,
      trackState,
      searchQuery,
      filteredTracks,
      reviewedCount,
      reviewedPct,
      totalTracks: trackNames.length,
      toggleMood,
      hasMood,
      toggleReviewed,
      onToggle,
      displayName,
      moodColor,
      exportJson,
      copyYaml,
      clearStorage,
      statusMsg,
      autosaveMsg,
    };
  },
}).mount("#app");
