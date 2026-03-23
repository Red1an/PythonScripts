import sys
import time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # без GUI

VERTICES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
N = len(VERTICES)

# 1. МАТРИЦА СМЕЖНОСТИ
ADJ_MATRIX = [
#    Mon Tue Wed Thu Fri Sat Sun
    [ 0,  3,  0,  2,  0,  0,  0],
    [ 0,  0,  6,  0,  0,  2,  0],
    [ 0,  0,  0,  8,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  7,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  3,  0,  5],
    [ 1,  4,  0,  0,  0,  0,  0],
]

EDGES = [
    (i, j, ADJ_MATRIX[i][j])
    for i in range(N) for j in range(N)
    if ADJ_MATRIX[i][j] != 0
]

def print_adjacency_matrix(matrix, vertices):
    print("\n   МАТРИЦА СМЕЖНОСТИ   ")
    header = f"{'':>6}" + "".join(f"{v:>6}" for v in vertices)
    print(header)
    for i, row in enumerate(matrix):
        line = f"{vertices[i]:>6}" + "".join(f"{val:>6}" for val in row)
        print(line)

print_adjacency_matrix(ADJ_MATRIX, VERTICES)


# 2. СПИСОК РЁБЕР (edge list)
def build_edge_list(matrix, vertices):
    edge_list = []
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                edge_list.append((vertices[i], vertices[j], matrix[i][j]))
    return edge_list

EDGE_LIST = build_edge_list(ADJ_MATRIX, VERTICES)

def print_edge_list(edge_list):
    print("\n    СПИСОК РЁБЕР    ")
    print(f"{'От':<8} {'До':<8} {'Вес':>5}")
    print("-" * 22)
    for u, v, w in edge_list:
        print(f"{u:<8} {v:<8} {w:>5}")

print_edge_list(EDGE_LIST)

# 3. МАССИВ ЗАПИСЕЙ
def build_records(matrix, vertices):
    n = len(vertices)
    records = []
    for i in range(n):
        parents = []
        children = []
        in_weights = []
        out_weights = []
        for j in range(n):
            if matrix[j][i] != 0:
                parents.append(vertices[j])
                in_weights.append(matrix[j][i])
            if matrix[i][j] != 0:
                children.append(vertices[j])
                out_weights.append(matrix[i][j])
        records.append({
            'index': i,
            'name': vertices[i],
            'parents': parents,
            'children': children,
            'in_weights': in_weights,
            'out_weights': out_weights,
        })
    return records

RECORDS = build_records(ADJ_MATRIX, VERTICES)

def print_records(records):
    print("\n    МАССИВ ЗАПИСЕЙ    ")
    for r in records:
        print(f"\n  Индекс : {r['index']}")
        print(f"  Имя    : {r['name']}")
        parents_str = ', '.join(
            f"{p}({w})" for p, w in zip(r['parents'], r['in_weights'])
        ) or '—'
        children_str = ', '.join(
            f"{c}({w})" for c, w in zip(r['children'], r['out_weights'])
        ) or '—'
        print(f"  Предки (входящие рёбра)  : {parents_str}")
        print(f"  Потомки (исходящие рёбра): {children_str}")

print_records(RECORDS)

# 4. ВИЗУАЛИЗАЦИЯ ГРАФА
def visualize_graph(vertices, edges, filename="graph_variant3.png"):
    DG = nx.DiGraph()
    DG.add_nodes_from(range(len(vertices)))
    labels = {i: v for i, v in enumerate(vertices)}
    for i, j, w in edges:
        DG.add_edge(i, j, weight=w)

    pos = nx.shell_layout(DG)
    edge_labels = {(i, j): w for i, j, w in edges}

    plt.figure(figsize=(9, 7))
    plt.title("Граф — Вариант 3 (Дни недели)", fontsize=14, pad=15)
    nx.draw_networkx_nodes(DG, pos, node_size=1800, node_color='white',
                           edgecolors='black', linewidths=1.5)
    nx.draw_networkx_labels(DG, pos, labels, font_size=11)
    nx.draw_networkx_edges(DG, pos, arrows=True, arrowsize=20,
                           connectionstyle='arc3,rad=0.1',
                           edge_color='steelblue', width=1.8,
                           min_source_margin=28, min_target_margin=28)
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels,
                                 font_size=10, font_color='crimson')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=120)
    plt.close()

visualize_graph(VERTICES, EDGES)

# 5. 12 ПОДПРОГРАММ (по 4 для каждого представления)
# A) МАТРИЦА СМЕЖНОСТИ
def matrix_find_neighbors(matrix, vertices, vertex_name):
    idx = vertices.index(vertex_name)
    neighbors = []
    for j in range(len(matrix)):
        if matrix[idx][j] != 0 or matrix[j][idx] != 0:
            if vertices[j] != vertex_name and vertices[j] not in neighbors:
                neighbors.append(vertices[j])
    return neighbors

def matrix_is_chain(matrix, vertices, sequence):
    for k in range(len(sequence) - 1):
        i = vertices.index(sequence[k])
        j = vertices.index(sequence[k + 1])
        if matrix[i][j] == 0:
            return False
    return True

def matrix_heavy_vertices(matrix, vertices, threshold):
    result = []
    n = len(matrix)
    for i in range(n):
        total = sum(matrix[i]) + sum(matrix[r][i] for r in range(n))
        if total > threshold:
            result.append((vertices[i], total))
    return result

def matrix_edge_count(matrix):
    return sum(1 for i in range(len(matrix)) for j in range(len(matrix))
               if matrix[i][j] != 0)

#  B) СПИСОК РЁБЕР

def edgelist_find_neighbors(edge_list, vertex_name):
    neighbors = set()
    for u, v, w in edge_list:
        if u == vertex_name:
            neighbors.add(v)
        elif v == vertex_name:
            neighbors.add(u)
    return list(neighbors)

def edgelist_is_chain(edge_list, sequence):
    edge_set = {(u, v) for u, v, w in edge_list}
    for k in range(len(sequence) - 1):
        if (sequence[k], sequence[k + 1]) not in edge_set:
            return False
    return True

def edgelist_heavy_vertices(edge_list, vertices, threshold):
    weight_sum = {v: 0 for v in vertices}
    for u, v, w in edge_list:
        weight_sum[u] += w
        weight_sum[v] += w
    return [(v, s) for v, s in weight_sum.items() if s > threshold]

def edgelist_edge_count(edge_list):
    return len(edge_list)

# C) МАССИВ ЗАПИСЕЙ

def records_find_neighbors(records, vertex_name):
    for r in records:
        if r['name'] == vertex_name:
            return list(set(r['parents'] + r['children']))
    return []

def records_is_chain(records, sequence):
    rec_map = {r['name']: r for r in records}
    for k in range(len(sequence) - 1):
        if sequence[k + 1] not in rec_map[sequence[k]]['children']:
            return False
    return True

def records_heavy_vertices(records, threshold):
    result = []
    for r in records:
        total = sum(r['in_weights']) + sum(r['out_weights'])
        if total > threshold:
            result.append((r['name'], total))
    return result

def records_edge_count(records):
    return sum(len(r['out_weights']) for r in records)


# ДЕМОНСТРАЦИЯ ПОДПРОГРАММ
TEST_VERTEX = 'Tue'
TEST_CHAIN_YES = ['Sun', 'Mon', 'Tue', 'Wed']
TEST_CHAIN_NO  = ['Sun', 'Wed', 'Mon']
THRESHOLD = 10

print("\n РЕЗУЛЬТАТЫ ПОДПРОГРАММ")

print(f"  A. Матрица смежности    ")
print(f"A1. Соседи '{TEST_VERTEX}': {matrix_find_neighbors(ADJ_MATRIX, VERTICES, TEST_VERTEX)}")
print(f"A2. {TEST_CHAIN_YES} — цепь? {matrix_is_chain(ADJ_MATRIX, VERTICES, TEST_CHAIN_YES)}")
print(f"A2. {TEST_CHAIN_NO} — цепь? {matrix_is_chain(ADJ_MATRIX, VERTICES, TEST_CHAIN_NO)}")
print(f"A3. Вершины с суммой весов > {THRESHOLD}: {matrix_heavy_vertices(ADJ_MATRIX, VERTICES, THRESHOLD)}")
print(f"A4. Количество рёбер: {matrix_edge_count(ADJ_MATRIX)}")

print(f"\n    B. Список рёбер    ")
print(f"B1. Соседи '{TEST_VERTEX}': {edgelist_find_neighbors(EDGE_LIST, TEST_VERTEX)}")
print(f"B2. {TEST_CHAIN_YES} — цепь? {edgelist_is_chain(EDGE_LIST, TEST_CHAIN_YES)}")
print(f"B2. {TEST_CHAIN_NO} — цепь? {edgelist_is_chain(EDGE_LIST, TEST_CHAIN_NO)}")
print(f"B3. Вершины с суммой весов > {THRESHOLD}: {edgelist_heavy_vertices(EDGE_LIST, VERTICES, THRESHOLD)}")
print(f"B4. Количество рёбер: {edgelist_edge_count(EDGE_LIST)}")

print(f"\n    C. Массив записей    ")
print(f"C1. Соседи '{TEST_VERTEX}': {records_find_neighbors(RECORDS, TEST_VERTEX)}")
print(f"C2. {TEST_CHAIN_YES} — цепь? {records_is_chain(RECORDS, TEST_CHAIN_YES)}")
print(f"C2. {TEST_CHAIN_NO} — цепь? {records_is_chain(RECORDS, TEST_CHAIN_NO)}")
print(f"C3. Вершины с суммой весов > {THRESHOLD}: {records_heavy_vertices(RECORDS, THRESHOLD)}")
print(f"C4. Количество рёбер: {records_edge_count(RECORDS)}")

# 6. РАЗМЕР В БАЙТАХ
def deep_size_matrix(matrix):
    total = sys.getsizeof(matrix)
    for row in matrix:
        total += sys.getsizeof(row)
        for val in row:
            total += sys.getsizeof(val)
    return total

def deep_size_edge_list(edge_list):
    total = sys.getsizeof(edge_list)
    for tpl in edge_list:
        total += sys.getsizeof(tpl)
        for x in tpl:
            total += sys.getsizeof(x)
    return total

def deep_size_records(records):
    total = sys.getsizeof(records)
    for r in records:
        total += sys.getsizeof(r)
        for k, v in r.items():
            total += sys.getsizeof(k) + sys.getsizeof(v)
            if isinstance(v, list):
                for item in v:
                    total += sys.getsizeof(item)
    return total

size_matrix   = deep_size_matrix(ADJ_MATRIX)
size_edgelist = deep_size_edge_list(EDGE_LIST)
size_records  = deep_size_records(RECORDS)

print("\n РАЗМЕР ОБЪЕКТОВ В БАЙТАХ")
print(f"Матрица смежности : {size_matrix} байт")
print(f"Список рёбер      : {size_edgelist} байт")
print(f"Массив записей    : {size_records} байт")

# 7. ЗАМЕР ВРЕМЕНИ (10^5 повторов)
REPEATS = 100_000

def measure(func, *args):
    start = time.perf_counter()
    for _ in range(REPEATS):
        func(*args)
    return (time.perf_counter() - start) / REPEATS * 1e6  # мкс

print(f" \n СРЕДНЕЕ ВРЕМЯ ВЫПОЛНЕНИЯ")
funcs = {
    "A1 matrix_find_neighbors":    (matrix_find_neighbors, ADJ_MATRIX, VERTICES, TEST_VERTEX),
    "A2 matrix_is_chain":          (matrix_is_chain, ADJ_MATRIX, VERTICES, TEST_CHAIN_YES),
    "A3 matrix_heavy_vertices":    (matrix_heavy_vertices, ADJ_MATRIX, VERTICES, THRESHOLD),
    "A4 matrix_edge_count":        (matrix_edge_count, ADJ_MATRIX),
    "B1 edgelist_find_neighbors":  (edgelist_find_neighbors, EDGE_LIST, TEST_VERTEX),
    "B2 edgelist_is_chain":        (edgelist_is_chain, EDGE_LIST, TEST_CHAIN_YES),
    "B3 edgelist_heavy_vertices":  (edgelist_heavy_vertices, EDGE_LIST, VERTICES, THRESHOLD),
    "B4 edgelist_edge_count":      (edgelist_edge_count, EDGE_LIST),
    "C1 records_find_neighbors":   (records_find_neighbors, RECORDS, TEST_VERTEX),
    "C2 records_is_chain":         (records_is_chain, RECORDS, TEST_CHAIN_YES),
    "C3 records_heavy_vertices":   (records_heavy_vertices, RECORDS, THRESHOLD),
    "C4 records_edge_count":       (records_edge_count, RECORDS),
}

for name, args in funcs.items():
    t = measure(args[0], *args[1:])
    print(f"  {name:<35} {t:>8.4f} мкс")