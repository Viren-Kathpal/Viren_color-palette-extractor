import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from color_palette_extractor import extract_colors
import matplotlib.pyplot as plt 

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if filepath:
        show_selected_image(filepath)
        hex_colors = extract_colors(filepath)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Dominant Colors:\n")
        for color in hex_colors:
            result_text.insert(tk.END, f"{color}\n")

        # Show color bar image after processing
        bar_path = os.path.join("output", f"{os.path.splitext(os.path.basename(filepath))[0]}_palette.png")
        if os.path.exists(bar_path):
            img = Image.open(bar_path)
            img = img.resize((400, 50))
            bar_img = ImageTk.PhotoImage(img)
            bar_label.config(image=bar_img)
            bar_label.image = bar_img
        else:
            messagebox.showwarning("Missing", "Color bar image not found!")

def show_selected_image(path):
    img = Image.open(path)
    img.thumbnail((300, 300))
    photo = ImageTk.PhotoImage(img)
    img_label.config(image=photo)
    img_label.image = photo

# GUI Layout
root = tk.Tk()
root.title("Color Palette Extractor")
root.geometry("600x600")
root.configure(bg="white")

title = tk.Label(root, text="Dominant Color Extractor", font=("Helvetica", 16, "bold"), bg="white")
title.pack(pady=10)

btn = tk.Button(root, text="Choose Image", command=open_file, font=("Helvetica", 12), bg="#3498db", fg="white")
btn.pack(pady=10)

img_label = tk.Label(root, bg="white")
img_label.pack(pady=10)

bar_label = tk.Label(root, bg="white")
bar_label.pack(pady=10)

result_text = tk.Text(root, height=10, width=40, font=("Courier", 10), bg="#f9f9f9")
result_text.pack(pady=10)

root.mainloop()