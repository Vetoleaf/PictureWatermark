import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Function to choose an image using a file dialog
def choose_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        load_image(file_path)

# Function to load and display the chosen image
def load_image(file_path):
    # Store the file path in a global variable
    img_label.file_path = file_path
    # Open and resize the image to fit the canvas
    image = Image.open(file_path).resize((600, 400))
    # Create an ImageTk object to display the image in a Tkinter Label
    img_label.image = ImageTk.PhotoImage(image)
    img_label.config(image=img_label.image)

# Function to apply a watermark to the loaded image and save it
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

        # Load a custom font and calculate the position for the watermark text
        custom_font = ImageFont.truetype("SANFW.ttf", size=font_size_value)
        text_width, text_height = draw.textsize(text, font=custom_font)
        position = ((image.width - text_width) // 2, (image.height - text_height) // 2)

        # Draw the watermark text with white color and 50% opacity
        draw.text(position, text, fill=(255, 255, 255, 128), font=custom_font)

        # Save the image with the watermark
        output_path = "output_image_with_watermark.jpg"
        image.save(output_path)
        messagebox.showinfo("Image Saved", f"The image with watermark has been saved to {output_path}")

# Function to handle the behavior when an entry field gains focus
def on_entry_click(event, entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")

# Function to handle the behavior when an entry field loses focus
def on_entry_focusout(event, entry, placeholder_text):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="gray")

# Create the main tkinter window
root = tk.Tk()
root.title("Watermark App")
root.geometry("680x600")

# Create a canvas for displaying the loaded image
canvas = tk.Canvas(root, width=600, height=400)
canvas.grid(row=0, column=0, columnspan=4)

# Create a label to display the image
img_label = tk.Label(canvas)
img_label.pack()

# Create buttons and entry fields for choosing an image, font size, watermark text, and applying a watermark
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

# Start the Tkinter main loop
root.mainloop()
