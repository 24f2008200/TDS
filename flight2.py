from haversine import haversine, Unit
import heapq
from collections import defaultdict

# -----------------------------
# Coordinates (only needed cities)
# -----------------------------
coords = {
    "Singapore": (1.3521, 103.8198),
    "Bangkok": (13.7563, 100.5018),
    "Dubai": (25.276987, 55.296249),
    "Doha": (25.276987, 51.520008),
    "Istanbul": (41.0082, 28.9784),
    "Athens": (37.9838, 23.7275),
    "Rome": (41.9028, 12.4964),
    "Vienna": (48.2082, 16.3738),
}

# -----------------------------
# Directed flight edges
# -----------------------------
edges = [
    ("Singapore", "Bangkok"),
    ("Dubai", "Singapore"),
    ("Dubai", "Bangkok"),
    ("Singapore", "Dubai"),
    ("Dubai", "Doha"),
    ("Doha", "Istanbul"),
    ("Istanbul", "Athens"),
    ("Athens", "Rome"),
    ("Rome", "Vienna"),
]

# -----------------------------
# Build weighted graph
# -----------------------------
graph = defaultdict(list)

for src, dst in edges:
    dist = haversine(coords[src], coords[dst], unit=Unit.KILOMETERS)
    graph[src].append((dst, dist))

# -----------------------------
# Dijkstra
# -----------------------------
def dijkstra(graph, start, end):
    pq = [(0, start, [])]
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        path = path + [node]

        if node == end:
            return cost, path

        for nxt, w in graph.get(node, []):
            if nxt not in visited:
                heapq.heappush(pq, (cost + w, nxt, path))

    return float("inf"), []

# -----------------------------
# Run
# -----------------------------
distance, path = dijkstra(graph, "Singapore", "Vienna")

print("Path:", " -> ".join(path))
print(f"Distance: {distance:.2f} km")
