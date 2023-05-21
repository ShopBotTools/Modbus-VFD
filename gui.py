import tkinter as tk
from tkinter import font

root = tk.Tk()  # create a root widget

FONT_SIZE = font.Font(size=15)
WINDOW_BACKGROUND = "white"
FONT_BACKGROUND = "white"
X_PADDING = 10

root.title("Spindle Control")
root.config(background=WINDOW_BACKGROUND)
root.minsize(100, 100)  # width, height
root.maxsize(1000, 1000)
root.geometry("700x150+50+50")  # width x height + x + y

# print(f"Current        :  {current/X_PADDING}A")
# print(f"Frequency      :  {float(hirz/100)}Hz")
# print(f"Output Voltage :  {volt}V")
# print(f"DC Bus Voltage :  {bus}V")
# print(f"Total Power    :  {power/X_PADDING}kW")
# print(f"Operation Code :  {process}")

#Column 1, Keys
current = tk.Label(root, text="Current", bg=FONT_BACKGROUND, font=FONT_SIZE, anchor="w")
current.grid(row=1, column=1, padx=X_PADDING)

frequency = tk.Label(root, text="Frequency", bg=FONT_BACKGROUND, font=FONT_SIZE)
frequency.grid(row=2, column=1, padx=X_PADDING)

output_voltage = tk.Label(root, text="Output Voltage", bg=FONT_BACKGROUND, font=FONT_SIZE)
output_voltage.grid(row=3, column=1, padx=X_PADDING)

dc_voltage = tk.Label(root, text="DC Bus Voltage", bg=FONT_BACKGROUND, font=FONT_SIZE)
dc_voltage.grid(row=4, column=1, padx=X_PADDING)

total_power = tk.Label(root, text="Total Power", bg=FONT_BACKGROUND, font=FONT_SIZE)
total_power.grid(row=5, column=1, padx=X_PADDING)

operation_code = tk.Label(root, text="Operation Code", bg=FONT_BACKGROUND, font=FONT_SIZE)
operation_code.grid(row=6, column=1, padx=X_PADDING)

#Column 2, Values
current = tk.Label(root, text="Current Value", bg=FONT_BACKGROUND, font=FONT_SIZE, anchor="w")
current.grid(row=1, column=2, padx=X_PADDING)

frequency = tk.Label(root, text="Frequency Value", bg=FONT_BACKGROUND, font=FONT_SIZE)
frequency.grid(row=2, column=2, padx=X_PADDING)

output_voltage = tk.Label(root, text="Output Voltage Value", bg=FONT_BACKGROUND, font=FONT_SIZE)
output_voltage.grid(row=3, column=2, padx=X_PADDING)

dc_voltage = tk.Label(root, text="DC Bus Voltage Value", bg=FONT_BACKGROUND, font=FONT_SIZE)
dc_voltage.grid(row=4, column=2, padx=X_PADDING)

total_power = tk.Label(root, text="Total Power Value", bg=FONT_BACKGROUND, font=FONT_SIZE)
total_power.grid(row=5, column=2, padx=X_PADDING)

operation_code = tk.Label(root, text="Operation Code Value", bg=FONT_BACKGROUND, font=FONT_SIZE)
operation_code.grid(row=6, column=2, padx=X_PADDING)
root.iconbitmap("rpm.ico")
root.mainloop()