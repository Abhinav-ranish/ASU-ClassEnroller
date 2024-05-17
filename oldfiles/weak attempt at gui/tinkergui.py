import tkinter as tk
from tkinter import messagebox
from Classsaverchromium import *



def display_message():
    messagebox.showinfo("Message", "Hello, this is a GUI application!")

def get_class_entries():
    entries = [entry.get() for entry in class_entries]
    print("Current values in class entry boxes:", entries)


def update_class_boxes(value):
    print("Updating class boxes...")
    num_classes = int(value)
    class_entries.clear() 
    
    for widget in class_boxes_frame.winfo_children():
        widget.destroy()  
        
    for i in range(num_classes):
        label = tk.Label(class_boxes_frame, text=f"Class {i+1}:")
        label.grid(row=i, column=0, padx=5, pady=5)
        class_entry = tk.Entry(class_boxes_frame)
        class_entry.grid(row=i, column=1, padx=5, pady=5)
        class_entries.append(class_entry)
    
    print(f"Number of class boxes updated: {num_classes}")


root = tk.Tk()
root.title("ASU Class Scraper")

label = tk.Label(root, text="Made by {pwn.crack} Nemesis")
label.pack(pady=10)

slider_label = tk.Label(root, text="Select number of classes to track:")
slider_label.pack()
slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, command=update_class_boxes)
slider.set(1)
slider.pack()

class_boxes_frame = tk.Frame(root)
class_boxes_frame.pack()

class_entries = []

update_class_boxes(slider.get())

button = tk.Button(root, text="Save entered values", command=get_class_entries)
button.pack(pady=5)


root.mainloop()
