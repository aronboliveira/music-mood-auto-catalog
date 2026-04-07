// moods-checks-sliced.js — Vue 3 app for Sliced Track Mood Assignments
// Depends on:
//   moods-checks-data.js        (ALL_MOODS, MOOD_COLORS)
//   moods-checks-sliced-data.js (SLICED_TRACK_MOODS, SLICED_PARTS)
//
// Each "track" here is a BASE NAME that groups all its parts.
// A single set of mood checkboxes applies to every part of that base name.
// On export the moods are expanded to every individual part filename.

const { createApp, ref, computed, onMounted, onBeforeUnmount, nextTick } = Vue;

const STORAGE_KEY = "moods-checks-sliced-state-v1";
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
    console.warn("moods-checks-sliced: localStorage write failed", e);
    return false;
  }
}

createApp({
  setup() {
    // ── Build reactive track list (base names only) ──────────────────────
    const trackNames = Object.keys(SLICED_TRACK_MOODS).sort((a, b) => {
      const strip = (s) => s.replace(/^[\d.\-\s]+/, "").toLowerCase();
      return strip(a).localeCompare(strip(b));
    });

    const trackState = ref({});
    let _dirty = false;

    // Pre-reviewed sliced tracks from data
    const PRE_REVIEWED_SLICED =
      typeof SLICED_REVIEWED_TRACKS !== "undefined"
        ? new Set(SLICED_REVIEWED_TRACKS)
        : new Set();

    trackNames.forEach((name) => {
      trackState.value[name] = {
        reviewed: PRE_REVIEWED_SLICED.has(name),
        open: false,
        moods: new Set(SLICED_TRACK_MOODS[name] || []),
      };
    });

    // ── Restore from localStorage ───────────────────────────────────────
    function restoreAll() {
      const saved = readStorage();
      if (!saved || typeof saved !== "object") return;

      const storedVersion = saved.__data_version__;
      const versionMatch =
        typeof SLICED_DATA_VERSION !== "undefined"
          ? storedVersion === SLICED_DATA_VERSION
          : true; // no version constant → trust localStorage

      for (const [track, entry] of Object.entries(saved)) {
        if (track.startsWith("__")) continue;
        if (!trackState.value[track]) continue;
        const ts = trackState.value[track];

        if (typeof entry.open === "boolean") ts.open = entry.open;

        if (versionMatch) {
          if (typeof entry.reviewed === "boolean") ts.reviewed = entry.reviewed;
          if (Array.isArray(entry.moods)) ts.moods = new Set(entry.moods);
        } else {
          // Version mismatch: data.js moods authoritative, union reviewed
          if (typeof entry.reviewed === "boolean" && entry.reviewed) {
            ts.reviewed = true;
          }
        }
      }

      // Enforce PRE_REVIEWED_SLICED
      for (const name of PRE_REVIEWED_SLICED) {
        if (trackState.value[name]) trackState.value[name].reviewed = true;
      }

      if (!versionMatch) {
        _dirty = true;
      }
    }

    function serializeState() {
      const state = {
        __data_version__:
          typeof SLICED_DATA_VERSION !== "undefined"
            ? SLICED_DATA_VERSION
            : undefined,
      };
      for (const [track, ts] of Object.entries(trackState.value)) {
        state[track] = {
          reviewed: ts.reviewed,
          open: ts.open,
          moods: Array.from(ts.moods),
        };
      }
      return state;
    }

    // ── Save ────────────────────────────────────────────────────────────
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

    // ── Interval auto-save ──────────────────────────────────────────────
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
    function bindDomListeners() {
      document
        .querySelectorAll('.reviewed-cb, .mood-grid input[type="checkbox"]')
        .forEach((el) => {
          if (el.dataset.moodsBound === "1") return;
          el.dataset.moodsBound = "1";
          el.addEventListener("change", () => {
            markDirty();
            saveAll();
          });
        });
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
      return trackNames.filter((n) => displayName(n).toLowerCase().includes(q));
    });

    // ── Reviewed stats ──────────────────────────────────────────────────
    const reviewedCount = computed(
      () => Object.values(trackState.value).filter((ts) => ts.reviewed).length,
    );
    const reviewedPct = computed(() =>
      ((reviewedCount.value / trackNames.length) * 100).toFixed(1),
    );

    // ── Toggle helpers ──────────────────────────────────────────────────
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

    function toggleReviewed(track) {
      trackState.value[track].reviewed = !trackState.value[track].reviewed;
      markDirty();
      saveAll();
    }

    function onToggle(track, ev) {
      trackState.value[track].open = ev.target.open;
      markDirty();
    }

    // ── Display helpers ─────────────────────────────────────────────────
    // Strip trailing "-part" (all sliced base names end with it), then
    // replace remaining hyphens/underscores with spaces.
    function displayName(baseName) {
      return baseName
        .replace(/-part$/i, "")
        .replace(/[-_]/g, " ")
        .trim();
    }

    function moodColor(mood) {
      return MOOD_COLORS[mood] || "#ccc";
    }

    function partCount(baseName) {
      return (SLICED_PARTS[baseName] || []).length;
    }

    // ── Collect and EXPAND for export ───────────────────────────────────
    // Each base name's moods are applied to every individual part filename.
    function collectExpanded() {
      const result = {};
      for (const [baseName, ts] of Object.entries(trackState.value)) {
        const moods = Array.from(ts.moods).sort();
        if (!moods.length) continue;
        const parts = SLICED_PARTS[baseName] || [];
        for (const partFile of parts) {
          result[partFile] = moods;
        }
      }
      return result;
    }

    // ── Export JSON (expanded — all part filenames) ─────────────────────
    const statusMsg = ref("");

    function exportJson() {
      saveAll();
      const data = collectExpanded();
      const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: "application/json",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "track-moods-sliced.json";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      statusMsg.value =
        "JSON exported ✓ (" + Object.keys(data).length + " parts)";
      setTimeout(() => (statusMsg.value = ""), 4000);
    }

    // ── Copy YAML (base names — compact review reference) ───────────────
    function copyYaml() {
      saveAll();
      const lines = Object.entries(trackState.value)
        .filter(([, ts]) => ts.moods.size)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([base, ts]) => {
          const moods = Array.from(ts.moods).sort();
          return (
            base + " [×" + partCount(base) + "]:\n  - " + moods.join("\n  - ")
          );
        })
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
      nextTick(() => {
        bindDomListeners();
        setTimeout(bindDomListeners, 500);
      });
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
      partCount,
      exportJson,
      copyYaml,
      clearStorage,
      statusMsg,
      autosaveMsg,
    };
  },
}).mount("#app");
