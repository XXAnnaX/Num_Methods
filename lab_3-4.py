import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
import math

# Метод лінійної регресії 
def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    mean_x = sum_x / n
    mean_y = sum_y / n

    sum_xy_deviation = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    sum_xx_deviation = sum((x[i] - mean_x) ** 2 for i in range(n))
    
    a = sum_xy_deviation / sum_xx_deviation
    b = mean_y - a * mean_x
    return a, b

# Логарифмування
def log_manual(value):
    return math.log(value)

# Експоненціальна функція
def exp_manual(value):
    return math.exp(value)

# Експоненціальна регресія
def exponential_regression(x, y):
    if any(yi <= 0 for yi in y):
        raise ValueError("Усі значення y повинні бути додатними для експоненціальної регресії")
    
    log_y = [log_manual(yi) for yi in y]
    b, log_a = linear_regression(x, log_y)
    a = exp_manual(log_a)
    return a, b

# Поліном Лагранжа
def lagrange_interpolation(x, y, x_interp):
    n = len(x)
    L = np.zeros_like(x_interp)
    for i in range(n):
        l_i = np.ones_like(x_interp)
        for j in range(n):
            if i != j:
                l_i *= (x_interp - x[j]) / (x[i] - x[j])
        L += y[i] * l_i
    return L

# Оновлення графіка
def update_plot(x, y, method):
    ax.clear()
    ax.scatter(x, y, color='red', label='Експериментальні точки')
    
    if method == 1:
        a, b = linear_regression(x, y)
        y_pred = a * x + b
        ax.plot(x, y_pred, color='blue', label=f'Лінійна регресія: y = {a:.2f}x + {b:.2f}')
    elif method == 2:
        a, b = exponential_regression(x, y)
        y_pred = a * np.exp(b * x)
        ax.plot(x, y_pred, color='green', label=f'Експ. регресія: y = {a:.2f}e^({b:.2f}x)')
    elif method == 3:
        x_interp = np.linspace(min(x), max(x), 500)
        y_interp = lagrange_interpolation(x, y, x_interp)
        ax.plot(x_interp, y_interp, color='purple', label='Поліном Лагранжа')
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    canvas.draw()

# Обробка даних
def solve():
    try:
        x_data = list(map(float, entry_x.get().split()))
        y_data = list(map(float, entry_y.get().split()))

        if len(x_data) != len(y_data):
            raise ValueError("Кількість x і y повинна збігатися")

        x = np.array(x_data)
        y = np.array(y_data)

        method = var_method.get()
        update_plot(x, y, method)

    except ValueError as e:
        messagebox.showerror("Помилка", f"Некоректні дані: {str(e)}")

# Інтерфейс
root = tk.Tk()
root.title("Регресія та інтерполяція")

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Введіть значення x (через пробіл):").grid(row=0, column=0)
entry_x = tk.Entry(frame, width=50)
entry_x.grid(row=0, column=1)
entry_x.insert(0, "57 60 65 70 75 84 90 105")

tk.Label(frame, text="Введіть значення y (через пробіл):").grid(row=1, column=0)
entry_y = tk.Entry(frame, width=50)
entry_y.grid(row=1, column=1)
entry_y.insert(0, "67 71 76 80 86 93 99 114")

# Вибір методу регресії
var_method = tk.IntVar(value=1)
tk.Radiobutton(frame, text="Лінійна регресія", variable=var_method, value=1).grid(row=2, column=0)
tk.Radiobutton(frame, text="Експоненціальна регресія", variable=var_method, value=2).grid(row=2, column=1)
tk.Radiobutton(frame, text="Поліном Лагранжа", variable=var_method, value=3).grid(row=3, columnspan=2)

tk.Button(frame, text="Побудувати", command=solve).grid(row=4, columnspan=2)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
