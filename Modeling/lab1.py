"""
Лабораторная работа №1
Моделирование генераторов равномерно распределённых псевдослучайных чисел
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform


# ─────────────────────────────────────────────
# 1. Генераторы
# ─────────────────────────────────────────────

def multiplicative_congruential(N: int, seed: int | None = None) -> np.ndarray:
    A = 7 ** 5
    C = 0
    M = 2 ** 32 - 1
    Rn = seed if seed is not None else 1
    R = np.empty(N)
    for i in range(N):
        Rn = (A * Rn + C) % M
        R[i] = Rn / M
    return R


def fibonacci_lagged(N: int, a: int = 63, b: int = 31) -> np.ndarray:
    warmup = max(a, b)
    init = multiplicative_congruential(warmup + N)
    buf = list(init[:warmup])
    R = np.empty(N)
    for i in range(N):
        ra = buf[-a]
        rb = buf[-b]
        val = ra - rb if ra >= rb else ra - rb + 1.0
        R[i] = val
        buf.append(val)
    return R


def mersenne_twister(N: int, seed: int = 42) -> np.ndarray:
    rng = np.random.Generator(np.random.MT19937(seed=seed))
    return rng.random(N)


# ─────────────────────────────────────────────
# 2. Теоретические характеристики U(0,1)
# ─────────────────────────────────────────────

MU_THEORY  = 0.5
VAR_THEORY = 1 / 12
STD_THEORY = np.sqrt(1 / 12)


# ─────────────────────────────────────────────
# 3. Вспомогательные функции
# ─────────────────────────────────────────────

def get_stats(arr: np.ndarray) -> tuple[float, float, float]:
    return float(np.mean(arr)), float(np.var(arr, ddof=1)), float(np.std(arr, ddof=1))


def empirical_cdf(arr: np.ndarray):
    sorted_arr = np.sort(arr)
    n = len(sorted_arr)
    y = np.arange(1, n + 1) / n
    return sorted_arr, y


# ─────────────────────────────────────────────
# 4. Настройки
# ─────────────────────────────────────────────

GENERATOR_NAMES = [
    "МКГ (Мульт. конгруэнтный)",
    "ГФ (Фибоначчи с запазд.)",
    "МТ (Вихрь Мерсенна)",
]
SIZES  = [1000, 5000, 10000]
COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c"]


# ─────────────────────────────────────────────
# 5. Графики
# ─────────────────────────────────────────────

def plot_histograms(datasets: dict):
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    fig.suptitle("Гистограммы псевдослучайных чисел", fontsize=16, fontweight="bold")

    for row, (gen_name, color) in enumerate(zip(GENERATOR_NAMES, COLORS)):
        for col, N in enumerate(SIZES):
            ax = axes[row][col]
            data = datasets[gen_name][N]
            ax.hist(data, bins=30, color=color, alpha=0.7, edgecolor="white", linewidth=0.4)
            ax.axhline(N / 30, color="red", linewidth=1.2, linestyle="--", alpha=0.8,
                       label="Теоретический уровень")
            ax.set_title(f"{gen_name}\nN = {N}", fontsize=9)
            ax.set_xlabel("Значение", fontsize=8)
            ax.set_ylabel("Частота", fontsize=8)
            if col == 2:
                ax.legend(fontsize=7)

    plt.tight_layout()
    plt.savefig("histograms.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("✓ Гистограммы сохранены → histograms.png")


def plot_ecdf(datasets: dict):
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    fig.suptitle("Эмпирические функции распределения (ECDF)", fontsize=16, fontweight="bold")

    x_th = np.linspace(0, 1, 300)
    F_th = uniform.cdf(x_th)

    for row, (gen_name, color) in enumerate(zip(GENERATOR_NAMES, COLORS)):
        for col, N in enumerate(SIZES):
            ax = axes[row][col]
            data = datasets[gen_name][N]
            x_emp, y_emp = empirical_cdf(data)
            ax.step(x_emp, y_emp, color=color, linewidth=1.2, label="ECDF")
            ax.plot(x_th, F_th, color="red", linewidth=1.5,
                    linestyle="--", alpha=0.8, label="F(x) = x (теор.)")
            ax.set_title(f"{gen_name}\nN = {N}", fontsize=9)
            ax.set_xlabel("x", fontsize=8)
            ax.set_ylabel("F(x)", fontsize=8)
            if col == 0 and row == 0:
                ax.legend(fontsize=7)

    plt.tight_layout()
    plt.savefig("ecdf.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("✓ ECDF сохранены → ecdf.png")


def plot_scatter(datasets: dict):
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    fig.suptitle("Тест «Распределение на плоскости» (Rₙ vs Rₙ₊₁)",
                 fontsize=16, fontweight="bold")

    for row, (gen_name, color) in enumerate(zip(GENERATOR_NAMES, COLORS)):
        for col, N in enumerate(SIZES):
            ax = axes[row][col]
            data = datasets[gen_name][N]
            ax.scatter(data[:-1], data[1:], s=0.8, color=color, alpha=0.5)
            ax.set_title(f"{gen_name}\nN = {N}", fontsize=9)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_xlabel("Rₙ", fontsize=8)
            ax.set_ylabel("Rₙ₊₁", fontsize=8)

    plt.tight_layout()
    plt.savefig("scatter.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("✓ Scatter-тест сохранён → scatter.png")


def plot_theoretical():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle("Теоретические характеристики U(0,1)", fontsize=14, fontweight="bold")

    x = np.linspace(-0.3, 1.3, 500)

    ax = axes[0]
    f = uniform.pdf(x)
    ax.plot(x, f, color="#1f77b4", linewidth=2.5)
    ax.fill_between(x, f, alpha=0.15, color="#1f77b4")
    ax.set_title("Плотность f(x)", fontsize=12)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.annotate("f(x) = 1, x ∈ [0,1]", xy=(0.5, 1.0), xytext=(0.5, 1.2),
                fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="#1f77b4"))
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    F = uniform.cdf(x)
    ax.plot(x, F, color="#ff7f0e", linewidth=2.5)
    ax.set_title("Функция распределения F(x)", fontsize=12)
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("theoretical.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("✓ Теоретические характеристики сохранены → theoretical.png")


def print_stats_table(datasets: dict):
    col_w = [30, 7, 14, 14, 14, 14, 14, 14]
    header = (
        f"{'Генератор':<{col_w[0]}} "
        f"{'N':>{col_w[1]}}  "
        f"{'Мат. ожид.':>{col_w[2]}}  "
        f"{'Дисперсия':>{col_w[3]}}  "
        f"{'СКО':>{col_w[4]}}  "
    )
    sep = "─" * len(header)
    print("\n" + sep)
    print(header)
    print(sep)

    for gen_name in GENERATOR_NAMES:
        for N in SIZES:
            mu, var, std = get_stats(datasets[gen_name][N])
            print(
                f"{gen_name:<{col_w[0]}} "
                f"{N:>{col_w[1]}}  "
                f"{mu:>{col_w[2]}.5f}  "
                f"{var:>{col_w[3]}.5f}  "
                f"{std:>{col_w[4]}.5f}  "
            )
        print(sep)


# ─────────────────────────────────────────────
# 6. Главная функция
# ─────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  ЛР №1 — Генераторы равномерно распределённых ПСЧ")
    print("=" * 60)

    print("\n▶  Генерация данных...")
    datasets: dict[str, dict[int, np.ndarray]] = {name: {} for name in GENERATOR_NAMES}

    for N in SIZES:
        datasets[GENERATOR_NAMES[0]][N] = multiplicative_congruential(N)
        datasets[GENERATOR_NAMES[1]][N] = fibonacci_lagged(N)
        datasets[GENERATOR_NAMES[2]][N] = mersenne_twister(N)
    print(f"   Готово. Наборов: {3 * 3}")

    print_stats_table(datasets)

    print(f"\nТеоретические значения для U(0,1):")
    print(f"  Математическое ожидание  M[X] = (a+b)/2    = {MU_THEORY:.6f}")
    print(f"  Дисперсия                D[X] = (b-a)²/12  = {VAR_THEORY:.6f}")
    print(f"  СКО                      σ[X] = (b-a)/√12  = {STD_THEORY:.6f}")

    print("\n▶  Построение графиков...")
    plot_theoretical()
    plot_histograms(datasets)
    plot_ecdf(datasets)
    plot_scatter(datasets)

    print("\n✅  Все задания выполнены.")


if __name__ == "__main__":
    main()