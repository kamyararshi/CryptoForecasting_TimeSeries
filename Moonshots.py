import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

root = tk.Tk()
root.title("Moonshots")
root.iconbitmap("python.ico")
root.geometry("1200x750")

var_main = tk.IntVar()
c_main = tk.Checkbutton(root, text="check this I dare u!", variable=var_main, onvalue="on", offvalue="off").grid(row=0, column=0, columnspan=2)





""" FRAME 1"""
frame_1 = tk.LabelFrame(root, text="This is my Frame", padx=10, pady=10)
frame_1.grid(row=1, column=1, padx=5, pady=5)
var = tk.IntVar()
c = tk.Checkbutton(frame_1, text="check frame 1!", variable=var, onvalue="on", offvalue="off").pack()

fig = plt.figure(figsize=(10, 5))
x = np.random.normal(25, 4, 100)
scatt = plt.scatter(x, np.arange(100), c='r', s=5)
canvas = FigureCanvasTkAgg(fig, master=frame_1)
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, frame_1)
toolbar.update()
# Pack
toolbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
""" End FRAME 1"""





""" FRAME 2"""
frame_2 = tk.LabelFrame(root, text="Options", padx=20, pady=90)
frame_2.grid(row=1, column=0, padx=5, pady=5)
btn =tk.Button(frame_2, text="Click").pack()









button_quit = tk.Button(master=root, text="Quit", command=root.quit).grid(row=4, column=0)


root.mainloop()