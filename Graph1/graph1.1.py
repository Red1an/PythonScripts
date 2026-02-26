import numpy as np
from collections import deque

A = np.array([
    [0, 3, 6, 5, 0],
    [3, 0, 2, 0, 4],
    [6, 2, 0, 1, 0],
    [5, 0, 1, 0, 7],
    [0, 4, 0, 7, 0]
], dtype=float)

n = len(A)

def incidence_matrix(A):
    n = len(A)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != 0:
                edges.append((i, j))

    B = np.zeros((n, len(edges)), dtype=int)
    for k, (i, j) in enumerate(edges):
        B[i][k] = 1
        B[j][k] = 1
    return B, edges


B, edges = incidence_matrix(A)
print("  Матрица инцидентности")
print("Рёбра:", [(i + 1, j + 1) for i, j in edges])
print(B)

def degree_matrix(A):
    degrees = np.sum(A, axis=1)
    return np.diag(degrees)


D = degree_matrix(A)
print("\n  Матрица степеней вершин")
print(D)

def reachability_matrix(A):
    n = len(A)
    R = np.eye(n, dtype=int)  # диагональ = 1 (путь до себя)

    for start in range(n):
        visited = set([start])
        queue = deque([start])
        while queue:
            v = queue.popleft()
            for u in range(n):
                if A[v][u] != 0 and u not in visited:
                    visited.add(u)
                    queue.append(u)
        for v in visited:
            R[start][v] = 1
    return R


R = reachability_matrix(A)
print("\n  Матрица достижимости")
print(R)

import heapq


def dijkstra(A, src):
    n = len(A)
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v in range(n):
            if A[u][v] != 0:
                nd = dist[u] + A[u][v]
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
    return dist


def distance_matrix(A):
    n = len(A)
    Dist = np.zeros((n, n))
    for i in range(n):
        Dist[i] = dijkstra(A, i)
    return Dist


Dist = distance_matrix(A)
print("\n  Матрица расстояний")
print(Dist)

def kirchhoff_matrix(A):
    D = np.diag(np.sum(A, axis=1))
    return D - A


K = kirchhoff_matrix(A)
print("\n  Матрица Киргофа")
print(K)