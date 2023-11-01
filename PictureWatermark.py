import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

def choose_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        load_image(file_path)

def load_image(file_path):
    img_label.file_path = file_path
    image = Image.open(file_path).resize((600, 400))
    img_label.image = ImageTk.PhotoImage(image)
    img_label.config(image=img_label.image)

def apply_watermark():
    if hasattr(img_label, 'file_path'):
        image = Image.open(img_label.file_path)
        draw = ImageDraw.Draw(image)
        text = watermark_text.get()
        font_size_input = font_size.get()

        try:
            font_size_value = int(font_size_input)
            if font_size_value <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Font Size", "Font Size must be a positive integer.")
            return

        custom_font = ImageFont.truetype("SANFW.ttf", size=font_size_value)
        text_width, text_height = draw.textsize(text, font=custom_font)
        position = ((image.width - text_width) // 2, (image.height - text_height) // 2)

        draw.text(position, text, fill=(255, 255, 255, 128), font=custom_font)

        output_path = "output_image_with_watermark.jpg"
        image.save(output_path)
        messagebox.showinfo("Image Saved", f"The image with watermark has been saved to {output_path}")

def on_entry_click(event, entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def on_entry_focusout(event, entry, placeholder_text):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="gray")

root = tk.Tk()
root.title("Watermark App")
root.geometry("680x600")

canvas = tk.Canvas(root, width=600, height=400)
canvas.grid(row=0, column=0, columnspan=4)

img_label = tk.Label(canvas)
img_label.pack()

choose_button = tk.Button(root, text="Choose Image", command=choose_image)
font_size = tk.Entry(root, fg="gray")
font_size.insert(0, "Font Size")
watermark_text = tk.Entry(root, fg="gray")
watermark_text.insert(0, "Watermark Text")
watermark_button = tk.Button(root, text="Apply Watermark", command=apply_watermark)

# Bind events for placeholder behavior
for entry, placeholder_text in [(font_size, "Font Size"), (watermark_text, "Watermark Text")]:
    entry.bind("<FocusIn>", lambda event, entry=entry, placeholder_text=placeholder_text: on_entry_click(event, entry, placeholder_text))
    entry.bind("<FocusOut>", lambda event, entry=entry, placeholder_text=placeholder_text: on_entry_focusout(event, entry, placeholder_text))

# Center-align buttons and entry fields horizontally
choose_button.grid(row=1, column=0, padx=(100, 0), pady=10)
font_size.grid(row=1, column=1, padx=10, pady=10)
watermark_text.grid(row=1, column=2, padx=10, pady=10)
watermark_button.grid(row=1, column=3, padx=(0, 100), pady=10)

# Keep the entry fields and buttons fixed at 150 pixels from the bottom
root.grid_rowconfigure(2, minsize=150)

root.mainloop()
