from tkinter import *

root = Tk()  # create a root widget
root.title("Spindle Control")
root.config(background="white")
root.minsize(100, 100)  # width, height
root.maxsize(1000, 1000)
root.geometry("700x150+50+50")  # width x height + x + y

# print(f"Current        :  {current/10}A")
# print(f"Frequency      :  {float(hirz/100)}Hz")
# print(f"Output Voltage :  {volt}V")
# print(f"DC Bus Voltage :  {bus}V")
# print(f"Total Power    :  {power/10}kW")
# print(f"Operation Code :  {process}")

# display_info = Label(root, text="", bg="white")
# display_info.grid(row=0, column=1, columnspan=2)
current_frame = Frame(root, bg="white")
current_frame.pack(side="left")
current_text = Label(current_frame, text="Current", bg="white", font=("Font", 15)).pack(side="left", padx=15)
frequency_text = Label(current_frame, text="Frequency", bg="white", font=("Font", 15)).pack(side="left", padx=15)

# text2.pack(side="left")
# text2 = Label(root, text="Output Voltage")
# text2.pack(side="left")
# text2 = Label(root, text="DC Bus Voltage")
# text2.pack(side="left")
# text2 = Label(root, text="Total Power")
# text2.pack(side="left")
# text2 = Label(root, text="Operation Code")
# text2.pack(side="left")
root.iconbitmap("rpm.ico")
root.mainloop()