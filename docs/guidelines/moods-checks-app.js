// moods-checks-app.js — Vue 3 app for Mood Assignments Checker
// Depends on: moods-checks-data.js (ALL_MOODS, MOOD_COLORS, TRACK_MOODS)

const { createApp, ref, computed, onMounted, onBeforeUnmount, nextTick } = Vue;

const STORAGE_KEY = "moods-checks-state-v2";
const SAVE_INTERVAL_MS = 5000;

// ── localStorage helpers ────────────────────────────────────────────────
function readStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function writeStorage(obj) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(obj));
    return true;
  } catch (e) {
    console.warn("moods-checks: localStorage write failed", e);
    return false;
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
    let _dirty = false; // marks unsaved changes

    // Pre-reviewed tracks from data.js
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
      if (!saved || typeof saved !== "object") return;

      const storedVersion = saved.__data_version__;
      const versionMatch = storedVersion === DATA_VERSION;

      for (const [track, entry] of Object.entries(saved)) {
        if (track.startsWith("__")) continue; // skip meta keys
        if (!trackState.value[track]) continue;
        const ts = trackState.value[track];

        // open/close state always restores
        if (typeof entry.open === "boolean") ts.open = entry.open;

        if (versionMatch) {
          // Same version: trust localStorage fully
          if (typeof entry.reviewed === "boolean") ts.reviewed = entry.reviewed;
          if (Array.isArray(entry.moods)) ts.moods = new Set(entry.moods);
        } else {
          // Version mismatch: data.js moods are authoritative.
          // For reviewed: union — keep true from either source.
          if (typeof entry.reviewed === "boolean" && entry.reviewed) {
            ts.reviewed = true;
          }
          // moods: keep data.js values (already set during initialisation)
        }
      }

      // After restore, always enforce PRE_REVIEWED as authoritative
      for (const name of PRE_REVIEWED) {
        if (trackState.value[name]) trackState.value[name].reviewed = true;
      }

      // If version changed, force a save to stamp new version
      if (!versionMatch) {
        _dirty = true;
      }
    }

    // ── Serialize state for saving ──────────────────────────────────────
    function serializeState() {
      const state = { __data_version__: DATA_VERSION };
      for (const [track, ts] of Object.entries(trackState.value)) {
        state[track] = {
          reviewed: ts.reviewed,
          open: ts.open,
          moods: Array.from(ts.moods),
        };
      }
      return state;
    }

    // ── Save to localStorage ────────────────────────────────────────────
    const autosaveMsg = ref("");

    function saveAll() {
      const ok = writeStorage(serializeState());
      if (ok) {
        _dirty = false;
        autosaveMsg.value = "saved " + new Date().toLocaleTimeString();
        setTimeout(() => (autosaveMsg.value = ""), 2000);
      }
    }

    function markDirty() {
      _dirty = true;
    }

    // ── Interval auto-save (every 5 s) ─────────────────────────────────
    let _intervalId = null;

    function startInterval() {
      if (_intervalId) return;
      _intervalId = setInterval(() => {
        if (_dirty) saveAll();
      }, SAVE_INTERVAL_MS);
    }

    function stopInterval() {
      if (_intervalId) {
        clearInterval(_intervalId);
        _intervalId = null;
      }
    }

    // ── DOM-level listeners with dataset guard ──────────────────────────
    // Attaches native change listeners to every checkbox so that
    // any mutation (even outside Vue) triggers markDirty + immediate save.
    // Uses el.dataset.moodsBound = "1" to guarantee at-most-once binding.
    function bindDomListeners() {
      document
        .querySelectorAll('.reviewed-cb, .mood-grid input[type="checkbox"]')
        .forEach((el) => {
          if (el.dataset.moodsBound === "1") return;
          el.dataset.moodsBound = "1";
          el.addEventListener("change", () => {
            markDirty();
            saveAll(); // immediate write on every checkbox toggle
          });
        });
      // Also bind <details> toggle events at DOM level
      document.querySelectorAll("details.track-details").forEach((el) => {
        if (el.dataset.moodsBound === "1") return;
        el.dataset.moodsBound = "1";
        el.addEventListener("toggle", () => {
          markDirty();
        });
      });
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
      markDirty();
      saveAll();
    }

    function hasMood(track, mood) {
      return trackState.value[track].moods.has(mood);
    }

    // ── Toggle reviewed ─────────────────────────────────────────────────
    function toggleReviewed(track) {
      trackState.value[track].reviewed = !trackState.value[track].reviewed;
      markDirty();
      saveAll();
    }

    // ── Toggle open ─────────────────────────────────────────────────────
    function onToggle(track, ev) {
      trackState.value[track].open = ev.target.open;
      markDirty();
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
      saveAll(); // flush before export
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
      saveAll(); // flush before copy
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
      _dirty = false;
      statusMsg.value = "Saved state cleared";
      setTimeout(() => (statusMsg.value = ""), 3000);
    }

    // ── Mount lifecycle ─────────────────────────────────────────────────
    onMounted(() => {
      restoreAll();
      startInterval();
      // Bind DOM-level listeners after Vue renders
      nextTick(() => {
        bindDomListeners();
        // Re-bind after a short delay (covers lazy-rendered elements)
        setTimeout(bindDomListeners, 500);
      });
      // Save on page hide / before unload
      window.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "hidden") saveAll();
      });
      window.addEventListener("beforeunload", () => saveAll());
    });

    onBeforeUnmount(() => {
      stopInterval();
      if (_dirty) saveAll();
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
