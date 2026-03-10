import numpy as np


def print_matrix(title, matrix, row_labels=None, col_labels=None):
    matrix = np.array(matrix)
    n_rows, n_cols = matrix.shape
    if row_labels is None:
        row_labels = [str(i+1) for i in range(n_rows)]
    if col_labels is None:
        col_labels = [str(i+1) for i in range(n_cols)]

    def fmt(val):
        if val == float('inf'):
            return 'inf'
        if isinstance(val, (float, np.floating)) and val == int(val):
            return str(int(val))
        return str(val)

    col_w = max(5, max(len(l) for l in col_labels) + 2)
    row_w = max(4, max(len(l) for l in row_labels) + 1)

    print(f"\n {title}")

    header = " " * (row_w + 1)
    for lbl in col_labels:
        header += lbl.center(col_w)
    print(header)

    for i in range(n_rows):
        line = row_labels[i].rjust(row_w) + " "
        for j in range(n_cols):
            line += fmt(matrix[i][j]).center(col_w)
        print(line)


G1 = np.array([
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0]
], dtype=int)

lbl_g1 = ['1', '2', '3', '4']
print_matrix("Исходный граф G1", G1, lbl_g1, lbl_g1)


def add_vertex_with_edge(A, connect_to):
    n = len(A)
    new_A = np.zeros((n + 1, n + 1), dtype=int)
    new_A[:n, :n] = A
    new_A[n][connect_to] = 1
    new_A[connect_to][n] = 1
    return new_A


G_after_add = add_vertex_with_edge(G1, connect_to=1)
lbl_add = ['1', '2', '3', '4', '5']
print_matrix("После добавления вершины 5 и ребра (5,2)", G_after_add, lbl_add, lbl_add)


def contract_vertices(A, v1_idx, v2_idx):
    n = len(A)
    new_A = A.copy()
    for i in range(n):
        if i != v1_idx and i != v2_idx:
            if new_A[v2_idx][i] == 1 or new_A[v1_idx][i] == 1:
                new_A[v1_idx][i] = 1
                new_A[i][v1_idx] = 1
    new_A[v1_idx][v1_idx] = 0
    new_A[v1_idx][v2_idx] = 0
    new_A[v2_idx][v1_idx] = 0
    new_A = np.delete(new_A, v2_idx, axis=0)
    new_A = np.delete(new_A, v2_idx, axis=1)
    return new_A


G_contracted = contract_vertices(G_after_add, v1_idx=2, v2_idx=3)
lbl_contracted = ['1', '2', "3'", '5']
print_matrix("После стягивания вершин 3 и 4", G_contracted, lbl_contracted, lbl_contracted)

G2 = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
], dtype=int)

lbl_g2 = ['5', '6', '7']
print_matrix("Исходный граф G2", G2, lbl_g2, lbl_g2)


def join_graphs(A1, A2):
    n1, n2 = len(A1), len(A2)
    n = n1 + n2
    result = np.zeros((n, n), dtype=int)
    result[:n1, :n1] = A1
    result[n1:, n1:] = A2
    for i in range(n1):
        for j in range(n1, n):
            result[i][j] = 1
            result[j][i] = 1
    return result


G_join = join_graphs(G_contracted, G2)
lbl_join = ["1", "2", "3'", "5(G1)", "5(G2)", "6", "7"]
print_matrix("Соединение графов G1 + G2", G_join, lbl_join, lbl_join)

D_join = np.diag(np.sum(G_join, axis=1))
print_matrix("Матрица степеней G1 + G2", D_join, lbl_join, lbl_join)