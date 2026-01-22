from haversine import haversine, Unit
import heapq
from collections import defaultdict

# -----------------------------
# City coordinates (lat, lon)
# -----------------------------
coords = {
    "New York": (40.7128, -74.006),
    "Los Angeles": (34.0522, -118.2437),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6895, 139.6917),
    "Osaka": (34.6937, 135.5023),
    "Paris": (48.8566, 2.3522),
    "New Delhi": (28.6139, 77.209),
    "Sydney": (33.8688, 151.2093),
    "Toronto": (43.65107, -79.347015),
    "Mexico City": (19.432608, -99.133209),
    "Shanghai": (31.2304, 121.4737),
    "Dubai": (25.276987, 55.296249),
    "Moscow": (55.7558, 37.6176),
    "Istanbul": (41.0082, 28.9784),
    "Mumbai": (19.076, 72.8777),
    "Bangkok": (13.7563, 100.5018),
    "Cape Town": (33.9249, 18.4241),
    "Singapore": (1.3521, 103.8198),
    "Hong Kong": (22.3193, 114.1694),
    "Barcelona": (41.3851, 2.1734),
    "Berlin": (52.52, 13.405),
    "Rome": (41.9028, 12.4964),
    "Chicago": (41.8781, -87.6298),
    "Buenos Aires": (34.6037, -58.3816),
    "Madrid": (40.4168, -3.7038),
    "San Francisco": (37.7749, -122.4194),
    "Rio de Janeiro": (22.9068, -43.1729),
    "Seoul": (37.5665, 126.978),
    "Santiago": (33.4489, -70.6693),
    "Lisbon": (38.7223, -9.1393),
    "Vienna": (48.2082, 16.3738),
    "Amsterdam": (52.3676, 4.9041),
    "Cairo": (30.0444, 31.2357),
    "Jakarta": (6.2088, 106.8456),
    "Lagos": (6.5244, 3.3792),
    "Kuala Lumpur": (3.139, 101.6869),
    "Vancouver": (49.2827, -123.1207),
    "Manila": (14.5995, 120.9842),
    "Athens": (37.9838, 23.7275),
    "Warsaw": (52.2297, 21.0122),
    "Budapest": (47.4979, 19.0402),
    "Helsinki": (60.1695, 24.9354),
    "Stockholm": (59.3293, 18.0686),
    "Brussels": (50.8503, 4.3517),
    "Prague": (50.0755, 14.4378),
    "Oslo": (59.9139, 10.7522),
    "Zurich": (47.3769, 8.5417),
    "Tel Aviv": (32.0853, 34.7818),
    "Doha": (25.276987, 51.520008),
    "Dublin": (53.3498, -6.2603),
}

# -----------------------------
# Directed flight edges
# -----------------------------
edges = [
    ("New York","London"), ("Tokyo","Sydney"), ("Paris","Berlin"),
    ("Dubai","Mumbai"), ("San Francisco","Tokyo"), ("Toronto","New York"),
    ("Shanghai","Singapore"), ("Los Angeles","Mexico City"),
    ("Istanbul","Athens"), ("Madrid","Rome"), ("Bangkok","Hong Kong"),
    ("Seoul","Shanghai"), ("Chicago","Toronto"), ("Cape Town","Nairobi"),
    ("Melbourne","Auckland"), ("Kuala Lumpur","Jakarta"),
    ("Rio de Janeiro","Buenos Aires"), ("Berlin","Prague"),
    ("Lima","Bogota"), ("Montreal","Miami"), ("Santiago","Lima"),
    ("Vancouver","San Francisco"), ("Boston","Dublin"),
    ("Oslo","Helsinki"), ("Sydney","Brisbane"),
    ("Singapore","Bangkok"), ("Zurich","Vienna"),
    ("Tokyo","Seoul"), ("Dubai","Tel Aviv"),
    ("Doha","Istanbul"), ("Athens","Cairo"),
    ("Lisbon","Madrid"), ("Warsaw","Budapest"),
    ("London","Paris"), ("Rome","Vienna"),
    ("Jakarta","Singapore"), ("Dubai","Doha"),
    ("Hong Kong","Tokyo"), ("Athens","Rome"),
    ("Berlin","Warsaw"), ("Vienna","Prague"),
    ("Lisbon","Dublin"), ("Helsinki","Stockholm"),
    ("Oslo","Brussels"), ("Zurich","Amsterdam"),
    ("Tel Aviv","Istanbul"), ("Tehran","Dubai"),
    ("Cairo","Dubai"), ("Dubai","Singapore"),
    ("Dubai","Bangkok")
]

# -----------------------------
# Build weighted graph
# -----------------------------
graph = defaultdict(list)

for src, dst in edges:
    if src in coords and dst in coords:
        dist = haversine(coords[src], coords[dst], unit=Unit.KILOMETERS)
        graph[src].append((dst, dist))

# -----------------------------
# Dijkstra shortest path
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
# Run query
# -----------------------------
distance, path = dijkstra(graph, "Singapore", "Vienna")

print("Path:", " -> ".join(path))
print(f"Distance: {distance:.2f} km")
