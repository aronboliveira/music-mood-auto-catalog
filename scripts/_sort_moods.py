#!/usr/bin/env python3
"""Sort 66 moods by emotional similarity using semantic clusters + NN intra-cluster."""
import math
import json

# 6D: (valence, arousal, dominance, darkness, longing, inwardness)
MOOD_VECTORS = {
    "Adventurous":   (0.6,  0.7,  0.7, -0.2,  0.0, -0.3),
    "Aggressive":    (-0.6,  0.9,  0.8,  0.6,  0.0, -0.5),
    "Anguished":     (-0.9,  0.5, -0.5,  0.8,  0.5,  0.4),
    "Awe-inspired":  (0.5,  0.3,  0.0, -0.1,  0.0,  0.2),
    "Bittersweet":   (-0.2, -0.1, -0.2,  0.3,  0.7,  0.5),
    "Brooding":      (-0.5, -0.1,  0.1,  0.7,  0.2,  0.7),
    "Chaotic":       (-0.3,  0.95, 0.3,  0.5,  0.0, -0.5),
    "Chill":         (0.4, -0.6,  0.0, -0.3,  0.0, -0.1),
    "Contemplative": (0.0, -0.4, -0.1,  0.1,  0.2,  0.8),
    "Cozy":          (0.7, -0.5, -0.1, -0.5,  0.1, -0.1),
    "Danceful":      (0.7,  0.8,  0.3, -0.5,  0.0, -0.6),
    "Dark":          (-0.6,  0.1,  0.2,  0.9,  0.0,  0.3),
    "Defiant":       (-0.2,  0.7,  0.8,  0.3,  0.0, -0.3),
    "Depressive":    (-0.9, -0.3, -0.7,  0.8,  0.3,  0.7),
    "Desperate":     (-0.8,  0.5, -0.5,  0.6,  0.5,  0.2),
    "Determined":    (0.2,  0.6,  0.8,  0.0,  0.0, -0.1),
    "Ecstatic":      (0.95, 0.9,  0.5, -0.7,  0.0, -0.5),
    "Emotional":     (-0.1,  0.2, -0.3,  0.2,  0.4,  0.5),
    "Energetic":     (0.5,  0.9,  0.5, -0.3,  0.0, -0.5),
    "Epic":          (0.4,  0.8,  0.9,  0.1,  0.0, -0.3),
    "Ethereal":      (0.2, -0.3, -0.2, -0.1,  0.1,  0.3),
    "Explosive":     (-0.3,  0.95, 0.7,  0.4,  0.0, -0.5),
    "Focused":       (0.1, -0.1,  0.5,  0.0,  0.0,  0.3),
    "Frenzy":        (-0.2,  0.95, 0.4,  0.4,  0.0, -0.5),
    "Furious":       (-0.8,  0.9,  0.7,  0.7,  0.0, -0.4),
    "Gritty":        (-0.3,  0.5,  0.5,  0.5,  0.0, -0.2),
    "Groovy":        (0.6,  0.6,  0.3, -0.4,  0.0, -0.4),
    "Hardworking":   (0.1,  0.5,  0.6,  0.0,  0.0,  0.0),
    "Heartbreak":    (-0.8,  0.1, -0.6,  0.5,  0.8,  0.5),
    "Heroic":        (0.5,  0.7,  0.9,  0.0,  0.0, -0.3),
    "Hypnotic":      (0.0,  0.0, -0.1,  0.2,  0.1,  0.4),
    "Introspective": (-0.1, -0.4, -0.2,  0.2,  0.3,  0.9),
    "Jaded":         (-0.4, -0.3,  0.0,  0.4,  0.2,  0.5),
    "Joyful":        (0.9,  0.7,  0.3, -0.7,  0.0, -0.4),
    "Lonely":        (-0.7, -0.4, -0.6,  0.5,  0.5,  0.7),
    "Macabre":       (-0.7,  0.2,  0.1,  0.95, 0.0,  0.1),
    "Meditative":    (0.2, -0.7, -0.2, -0.1,  0.0,  0.7),
    "Melancholic":   (-0.5, -0.3, -0.4,  0.4,  0.7,  0.6),
    "Mysterious":    (-0.1,  0.0,  0.1,  0.6,  0.0,  0.3),
    "Nostalgic":     (-0.1, -0.3, -0.3,  0.2,  0.8,  0.5),
    "Ominous":       (-0.5,  0.2,  0.3,  0.85, 0.0,  0.1),
    "Optimistic":    (0.7,  0.4,  0.3, -0.5,  0.0, -0.2),
    "Peaceful":      (0.6, -0.7,  0.0, -0.5,  0.0,  0.1),
    "Playful":       (0.8,  0.6,  0.2, -0.6,  0.0, -0.5),
    "Rebellious":    (-0.3,  0.7,  0.7,  0.4,  0.0, -0.3),
    "Relaxed":       (0.5, -0.6, -0.1, -0.4,  0.0,  0.0),
    "Resigned":      (-0.5, -0.5, -0.6,  0.3,  0.3,  0.5),
    "Reverent":      (0.3, -0.2,  0.0,  0.2,  0.1,  0.4),
    "Romantic":      (0.5,  0.1, -0.1, -0.2,  0.3,  0.1),
    "Sad":           (-0.7, -0.3, -0.5,  0.4,  0.4,  0.7),
    "Sensual":       (0.4,  0.2, -0.1, -0.1,  0.1,  0.0),
    "Serene":        (0.6, -0.7, -0.1, -0.5,  0.0,  0.2),
    "Sleepy":        (0.2, -0.9, -0.3, -0.2,  0.0,  0.0),
    "Soaring":       (0.6,  0.5,  0.4, -0.3,  0.0, -0.2),
    "Spiritual":     (0.3, -0.3,  0.0,  0.2,  0.1,  0.5),
    "Surreal":       (0.0,  0.0, -0.1,  0.3,  0.1,  0.3),
    "Suspenseful":   (-0.3,  0.4,  0.2,  0.6,  0.0,  0.0),
    "Tender":        (0.5, -0.2, -0.3, -0.2,  0.3,  0.2),
    "Tense":         (-0.4,  0.5,  0.2,  0.5,  0.0, -0.1),
    "Triumphant":    (0.7,  0.7,  0.9, -0.2,  0.0, -0.2),
    "Upbeat":        (0.7,  0.6,  0.2, -0.4,  0.0, -0.3),
    "Vengeful":      (-0.7,  0.7,  0.6,  0.8,  0.1, -0.2),
    "Whimsical":     (0.6,  0.3,  0.0, -0.5,  0.0, -0.1),
    "Wistful":       (-0.2, -0.3, -0.3,  0.2,  0.7,  0.5),
    "Yearning":      (-0.3,  0.1, -0.4,  0.3,  0.8,  0.4),
}

assert len(MOOD_VECTORS) == 65


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# ── Semantic clusters (ordered by emotional arc) ──
# Flow: Peaceful/Sleepy → Cozy/Tender → Romantic → Nostalgic/Yearning →
#       Reflective → Introspective → Tense → Sad/Lonely → Depressive →
#       Dark/Brooding → Mysterious/Surreal → Aggressive/Rebellious →
#       Energetic → Epic/Heroic → Determined/Focused → Joyful/Upbeat
CLUSTERS = [
    # calm/peaceful
    ["Peaceful", "Serene", "Relaxed", "Chill", "Sleepy"],
    # warm/tender → romantic
    ["Cozy", "Tender", "Romantic", "Sensual"],
    # nostalgic/longing
    ["Nostalgic", "Wistful", "Yearning", "Bittersweet", "Emotional"],
    # reflective
    ["Awe-inspired", "Reverent", "Spiritual", "Contemplative", "Meditative"],
    # introspective (bridge into darker territory)
    ["Introspective", "Jaded"],
    # tense/suspenseful
    ["Tense", "Suspenseful", "Gritty"],
    # sad/lonely
    ["Melancholic", "Sad", "Lonely", "Resigned", "Heartbreak"],
    # depressive
    ["Depressive", "Anguished", "Desperate"],
    # dark/brooding
    ["Brooding", "Dark", "Macabre", "Ominous"],
    # mysterious/surreal
    ["Mysterious", "Hypnotic", "Surreal", "Ethereal"],
    # aggressive/rebellious
    ["Aggressive", "Furious", "Vengeful", "Explosive", "Chaotic", "Frenzy",
     "Rebellious", "Defiant"],
    # energetic
    ["Energetic", "Danceful", "Groovy"],
    # heroic/epic
    ["Epic", "Heroic", "Triumphant", "Adventurous", "Soaring"],
    # determined/focused
    ["Determined", "Hardworking", "Focused"],
    # joyful/upbeat
    ["Ecstatic", "Joyful", "Playful", "Whimsical", "Upbeat", "Optimistic"],
]

# Verify all 66 moods are present
flat = [m for c in CLUSTERS for m in c]
assert sorted(flat) == sorted(MOOD_VECTORS.keys()), \
    f"Missing: {set(MOOD_VECTORS) - set(flat)}, Extra: {set(flat) - set(MOOD_VECTORS)}"

# ── Within each cluster, use NN to order by proximity ──


def nn_within(cluster):
    if len(cluster) <= 2:
        return cluster
    n = len(cluster)
    D = {}
    for i in range(n):
        for j in range(i+1, n):
            d = dist(MOOD_VECTORS[cluster[i]], MOOD_VECTORS[cluster[j]])
            D[(i, j)] = D[(j, i)] = d

    # Try every start, pick shortest path
    best_cost, best_order = float('inf'), None
    for start in range(n):
        visited = [False]*n
        order = [start]
        visited[start] = True
        for _ in range(n-1):
            curr = order[-1]
            nxt = min((j for j in range(n) if not visited[j]),
                      key=lambda j: D[(curr, j)])
            order.append(nxt)
            visited[nxt] = True
        cost = sum(D[(order[k], order[k+1])] for k in range(n-1))
        if cost < best_cost:
            best_cost = cost
            best_order = order
    return [cluster[i] for i in best_order]

# ── Connect cluster boundaries ──
# For each adjacent pair of clusters, orient the second cluster so
# that its nearest-to-previous-tail element is at its head.


def orient_cluster(prev_tail, cluster):
    """Return cluster ordered so the element closest to prev_tail is first."""
    ordered = nn_within(cluster)
    d_head = dist(MOOD_VECTORS[prev_tail], MOOD_VECTORS[ordered[0]])
    d_tail = dist(MOOD_VECTORS[prev_tail], MOOD_VECTORS[ordered[-1]])
    if d_tail < d_head:
        ordered.reverse()
    return ordered


result = nn_within(CLUSTERS[0])
for cluster in CLUSTERS[1:]:
    result.extend(orient_cluster(result[-1], cluster))

# ── Print result ──
print(f"Moods: {len(result)}\n")
for i, m in enumerate(result):
    v = MOOD_VECTORS[m]
    print(f"{i+1:2d}. {m:20s}  V={v[0]:+.2f} A={v[1]:+.2f} D={v[2]:+.2f} K={v[3]:+.2f} L={v[4]:+.2f} I={v[5]:+.2f}")

# Validate user examples


def pos(mood):
    return result.index(mood) + 1


print("\n=== Validation ===")
tests = [
    ("Nostalgic", ["Yearning", "Melancholic"]),
    ("Focused", ["Determined", "Triumphant"]),
    ("Sad", ["Introspective", "Lonely"]),
    ("Rebellious", ["Explosive", "Defiant", "Aggressive"]),
]
for anchor, neighbors in tests:
    gaps = [(n, abs(pos(anchor) - pos(n))) for n in neighbors]
    print(f"  {anchor} (#{pos(anchor)}): " +
          ", ".join(f"{n} (#{pos(n)}, gap={g})" for n, g in gaps))

print("\n=== JS ===")
js = json.dumps(result, indent=2)
print(f"const ALL_MOODS = {js};")
