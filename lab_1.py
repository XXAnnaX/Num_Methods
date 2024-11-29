import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
import math

# Функції для вибору
def f1(x):
    return 8 * x**2 - math.sin(10 * x)

def df1(x):
    return 16 * x - 10 * math.cos(10 * x)

def f2(x):
    if x <= 0:
        return float('inf')
    return x + math.log10(x) - 0.5

def df2(x):
    if x <= 0:
        return float('inf')
    return 1 + 1/(x * math.log(10))

# Метод дихотомії (подібний до бісекції)
def bisection_method(f, a, b, tol):
    iterations = []
    if f(a) * f(b) >= 0:
        messagebox.showerror("Помилка", "Знаки на межах інтервалу повинні бути різні!")
        return None, []
    
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        iterations.append((a, b, c, f(c)))
        if f(c) == 0 or (b - a) / 2 < tol:
            return c, iterations
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2, iterations

# Ітераційний метод
def iteration_method(f, x0, tol, max_iter=100):
    iterations = []
    for i in range(max_iter):
        x1 = f(x0)
        iterations.append((i, x0, f(x0)))
        if abs(x1 - x0) < tol:
            return x1, iterations
        x0 = x1
    messagebox.showwarning("Попередження", "Досягнуто максимальну кількість ітерацій")
    return x1, iterations

# Метод Ньютона
def newton_method(f, df, x0, tol, max_iter=100):
    iterations = []
    for i in range(max_iter):
        x1 = x0 - f(x0)/df(x0)
        iterations.append((i, x0, f(x0)))
        if abs(x1 - x0) < tol:
            return x1, iterations
        x0 = x1
    messagebox.showwarning("Попередження", "Досягнуто максимальну кількість ітерацій")
    return x1, iterations

# Відображення графіка
def update_plot(f, a, b):
    x_vals = np.linspace(a, b, 400)
    y_vals = [f(x) for x in x_vals]
    ax.clear()
    ax.plot(x_vals, y_vals, label="Графік функції")
    ax.axhline(0, color='black')
    canvas.draw()

# Головний алгоритм
def solve():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        tol = float(entry_tol.get())
        func = f1 if var_func.get() == 1 else f2
        d_func = df1 if var_func.get() == 1 else df2

        method = var_method.get()
        if method == 1:  # Метод дихотомії
            result, iterations = bisection_method(func, a, b, tol)
        elif method == 2:  # Ітераційний метод
            result, iterations = iteration_method(func, a, tol)
        elif method == 3:  # Метод Ньютона
            result, iterations = newton_method(func, d_func, a, tol)
        else:
            messagebox.showerror("Помилка", "Невідомий метод!")
            return

        if result:
            label_result.config(text=f"Знайдений корінь: {result:.6f}")
            update_plot(func, a, b)

            text_iterations.delete(1.0, tk.END)
            for i, data in enumerate(iterations):
                text_iterations.insert(tk.END, f"Ітерація {i+1}: {data}\n")
    except ValueError:
        messagebox.showerror("Помилка", "Некоректні дані")

# Інтерфейс
root = tk.Tk()
root.title("Чисельне розв'язання нелінійних рівнянь")

# Поля вводу
frame = tk.Frame(root)
frame.pack()
tk.Label(frame, text="Ліва межа:").grid(row=0, column=0)
entry_a = tk.Entry(frame)
entry_a.grid(row=0, column=1)
entry_a.insert(0, "0.1")

tk.Label(frame, text="Права межа:").grid(row=1, column=0)
entry_b = tk.Entry(frame)
entry_b.grid(row=1, column=1)
entry_b.insert(0, "0.4")

tk.Label(frame, text="Точність:").grid(row=2, column=0)
entry_tol = tk.Entry(frame)
entry_tol.grid(row=2, column=1)
entry_tol.insert(0, "0.0001")

# Вибір функції
var_func = tk.IntVar(value=1)
tk.Radiobutton(frame, text="8x^2 - sin(10x)", variable=var_func, value=1).grid(row=3, column=0)
tk.Radiobutton(frame, text="x + log10(x) - 0.5", variable=var_func, value=2).grid(row=3, column=1)

# Вибір методу
var_method = tk.IntVar(value=1)
tk.Radiobutton(frame, text="Метод дихотомії", variable=var_method, value=1).grid(row=4, column=0)
tk.Radiobutton(frame, text="Ітераційний метод", variable=var_method, value=2).grid(row=4, column=1)
tk.Radiobutton(frame, text="Метод Ньютона", variable=var_method, value=3).grid(row=5, column=0)

tk.Button(frame, text="Обчислити", command=solve).grid(row=6, columnspan=2)

# Відображення результатів
label_result = tk.Label(frame, text="Корінь:")
label_result.grid(row=7, columnspan=2)

text_iterations = tk.Text(root, height=10)
text_iterations.pack()

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
