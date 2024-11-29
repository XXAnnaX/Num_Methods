import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

# Функції для інтегрування
def f1(x):
    return 1 / np.sqrt(x - 1)

def f2(x):
    return np.sin(x) / (x + 1)

def f3(x):
    return 1 / np.sqrt(0.5 * x**2 + 1)

# Метод Монте-Карло
def monte_carlo_method_with_plot(f, a, b, N):
    # Генерація точок для знаходження максимуму функції на заданому проміжку
    x_vals = np.linspace(a, b, 10)
    y_vals = f(x_vals)
    
    # Фільтруємо нескінченні або некоректні значення
    y_vals = np.nan_to_num(y_vals, nan=0.0, posinf=0.0, neginf=0.0)
    y_max = max(y_vals)
    
    x_rand = np.random.uniform(a, b, N)
    y_rand = np.random.uniform(0, y_max, N)
    
    under_curve = y_rand <= f(x_rand)
    estimated_area = (b - a) * y_max * np.mean(under_curve)
    
    # Візуалізація
    ax.clear()
    x_vals = np.linspace(a, b, 400)
    ax.plot(x_vals, f(x_vals), label="Графік функції", color='blue')
    ax.scatter(x_rand[under_curve], y_rand[under_curve], color='green', s=1, label="Під графіком")
    ax.scatter(x_rand[~under_curve], y_rand[~under_curve], color='red', s=1, label="Над графіком")
    ax.legend()
    canvas.draw()
    
    return estimated_area

# Метод прямокутників
def square_method_with_plot(f, a, b, N):
    h = (b - a) / N
    x_vals = np.linspace(a, b, N+1)
    y_vals = f(x_vals)
    
    integral = np.sum(y_vals) * h
    
    # Візуалізація
    ax.clear()
    ax.plot(np.linspace(a, b, 400), f(np.linspace(a, b, 400)), label="Графік функції", color='blue')
    for x, y in zip(x_vals, y_vals):
        ax.bar(x, y, width=h, color='green', alpha=0.5, align='edge')
    ax.legend()
    canvas.draw()
    
    return integral

# Метод трапецій
def trapezoid_method_with_plot(f, a, b, N):
    h = (b - a) / N
    x_vals = np.linspace(a, b, N + 1)
    y_vals = f(x_vals)
    
    integral = h * (0.5 * y_vals[0] + np.sum(y_vals[1:-1]) + 0.5 * y_vals[-1])
    
    # Візуалізація
    ax.clear()
    ax.plot(np.linspace(a, b, 400), f(np.linspace(a, b, 400)), label="Графік функції", color='blue')
    ax.fill_between(x_vals, 0, y_vals, color='green', alpha=0.5, label="Трапеції")
    ax.legend()
    canvas.draw()
    
    return integral

# Обчислення інтегралів і оновлення результатів
def solve():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        N = int(entry_N.get())
        func = f1 if var_func.get() == 1 else f2 if var_func.get() == 2 else f3
        method = method_var.get()
        
        if method == 1:
            result = monte_carlo_method_with_plot(func, a, b, N)
            method_name = "Метод Монте-Карло"
        elif method == 2:
            result = square_method_with_plot(func, a, b, N)
            method_name = "Метод прямокутників"
        else:
            result = trapezoid_method_with_plot(func, a, b, N)
            method_name = "Метод трапецій"
        
        text_results.delete(1.0, tk.END)
        text_results.insert(tk.END, f"{method_name} (N={N}): {result:.6f}\n")
        
    except ValueError:
        messagebox.showerror("Помилка", "Некоректні дані")

# Інтерфейс
root = tk.Tk()
root.title("Чисельне інтегрування із графікою")

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Ліва межа:").grid(row=0, column=0)
entry_a = tk.Entry(frame)
entry_a.grid(row=0, column=1)
entry_a.insert(0, "1")

tk.Label(frame, text="Права межа:").grid(row=1, column=0)
entry_b = tk.Entry(frame)
entry_b.grid(row=1, column=1)
entry_b.insert(0, "3")

tk.Label(frame, text="Кількість поділів N:").grid(row=2, column=0)
entry_N = tk.Entry(frame)
entry_N.grid(row=2, column=1)
entry_N.insert(0, "10")

# Вибір функції
var_func = tk.IntVar(value=1)
tk.Radiobutton(frame, text="1/sqrt(x-1)", variable=var_func, value=1).grid(row=3, column=0)
tk.Radiobutton(frame, text="sin(x)/(x+1)", variable=var_func, value=2).grid(row=3, column=1)
tk.Radiobutton(frame, text="1/sqrt(0.5x^2+1)", variable=var_func, value=3).grid(row=4, column=0)

# Вибір методу
method_var = tk.IntVar(value=1)
tk.Radiobutton(frame, text="Монте-Карло", variable=method_var, value=1).grid(row=5, column=0)
tk.Radiobutton(frame, text="Прямокутників", variable=method_var, value=2).grid(row=5, column=1)
tk.Radiobutton(frame, text="Трапецій", variable=method_var, value=3).grid(row=6, column=0)

tk.Button(frame, text="Обчислити", command=solve).grid(row=7, columnspan=2)

text_results = tk.Text(root, height=5)
text_results.pack()

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
