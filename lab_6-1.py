import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

# Функція з варіанту
def default_function(x, y):
    return 2 * x - y

def dynamic_function(x, y):
    global user_function
    try:
        local_vars = {"x": x, "y": y, **vars(np)}
        return eval(user_function, local_vars)
    except Exception as e:
        raise ValueError(f"Некоректний вираз: {str(e)}")
    
# def analytical_solution(x, y0):
#     return 2 * x - 1 + (y0 + 1) * np.exp(-x)

# Метод Ейлера
def euler_method(f, x0, y0, xn, h):
    x_values = np.arange(x0, xn + h, h)
    y_values = [y0]
    for i in range(1, len(x_values)):
        y_values.append(y_values[-1] + h * f(x_values[i - 1], y_values[-1]))
    return x_values, np.array(y_values)

# Метод Рунге-Кутта 4-го порядку
def runge_kutta_4th(f, x0, y0, xn, h):
    x_values = np.arange(x0, xn + h, h)
    y_values = [y0]
    for i in range(1, len(x_values)):
        x_prev, y_prev = x_values[i - 1], y_values[-1]
        k1 = h * f(x_prev, y_prev)
        k2 = h * f(x_prev + h / 2, y_prev + k1 / 2)
        k3 = h * f(x_prev + h / 2, y_prev + k2 / 2)
        k4 = h * f(x_prev + h, y_prev + k3)
        y_values.append(y_prev + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    return x_values, np.array(y_values)

# Оновлення графіка
def update_plot(x0, y0, xn, h, method):
    ax.clear()
    ax.set_title("Чисельне розв'язання диференціального рівняння", fontsize=14)

    # if method == 0 or method > 0:
    #     x_analytical = np.linspace(x0, xn, 500)  
    #     y_analytical = analytical_solution(x_analytical, y0)
    #     ax.plot(x_analytical, y_analytical, 'k-', label="Аналітичний розв'язок")
  
    # Метод Ейлера
    if method == 1 or method == 3:
        x_euler, y_euler = euler_method(dynamic_function, x0, y0, xn, h)
        ax.plot(x_euler, y_euler, 'b-', label=f'Метод Ейлера (h={h})')

    # Метод Рунге-Кутта
    if method == 2 or method == 3:
        x_rk, y_rk = runge_kutta_4th(dynamic_function, x0, y0, xn, h)
        ax.plot(x_rk, y_rk, 'g-', label=f'Метод Рунге-Кутта (h={h})')

    # Оформлення графіка
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.legend()
    canvas.draw()

# Обробка даних з інтерфейсу
def solve():
    global user_function
    try:
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        xn = float(entry_xn.get())
        h = float(var_h.get())
        user_function = entry_function.get()  # Отримати функцію від користувача

        method = var_method.get()
        update_plot(x0, y0, xn, h, method)

    except ValueError as e:
        messagebox.showerror("Помилка", f"Некоректні дані: {str(e)}")

# Інтерфейс
root = tk.Tk()
root.title("Чисельне розв'язання диференціальних рівнянь")

frame = tk.Frame(root)
frame.pack()

# Поля введення
tk.Label(frame, text="x0:").grid(row=0, column=0)
entry_x0 = tk.Entry(frame)
entry_x0.grid(row=0, column=1)
entry_x0.insert(0, "0")

tk.Label(frame, text="y0:").grid(row=1, column=0)
entry_y0 = tk.Entry(frame)
entry_y0.grid(row=1, column=1)
entry_y0.insert(0, "1")

tk.Label(frame, text="xn:").grid(row=2, column=0)
entry_xn = tk.Entry(frame)
entry_xn.grid(row=2, column=1)
entry_xn.insert(0, "3")

tk.Label(frame, text="Функція f(x, y):").grid(row=3, column=0)
entry_function = tk.Entry(frame, width=30)
entry_function.grid(row=3, column=1, columnspan=2)
entry_function.insert(0, "2*x - y")  # Функція за замовчуванням

# Вибір кроку
tk.Label(frame, text="Виберіть крок h:").grid(row=4, column=0)
var_h = tk.StringVar(value="0.1")
tk.Radiobutton(frame, text="h = 0.1", variable=var_h, value="0.1").grid(row=4, column=1)
tk.Radiobutton(frame, text="h = 0.2", variable=var_h, value="0.2").grid(row=4, column=2)

# Вибір методу
tk.Label(frame, text="Метод:").grid(row=5, column=0)
var_method = tk.IntVar(value=3)
tk.Radiobutton(frame, text="Метод Ейлера", variable=var_method, value=1).grid(row=5, column=1)
tk.Radiobutton(frame, text="Метод Рунге-Кутта", variable=var_method, value=2).grid(row=5, column=2)
tk.Radiobutton(frame, text="Об'єднати", variable=var_method, value=3).grid(row=5, column=3)

tk.Button(frame, text="Розрахувати", command=solve).grid(row=6, columnspan=4)

# Графік
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Функція за замовчуванням
user_function = "2*x - y"

root.mainloop()
