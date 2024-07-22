import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import qrcode
from barcode import EAN13, Code128, Code39, UPCA, ISBN13, PZN, JAN, EAN8, ISBN10, ISSN, ITF, Gs1_128
from barcode.writer import ImageWriter
from pylibdmtx.pylibdmtx import encode as dmtx_encode
from PIL import Image, ImageTk, ImageDraw, ImageOps
from io import BytesIO
import pdf417gen
import pyqrcodeng

def generate_qr_code(data, version, error_correction, box_size, border, fill_color="black", back_color="white"):
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")
    return img

def generate_barcode(data, barcode_type='EAN13', module_width=0.2, module_height=15, font_size=10, text_distance=5, fill_color="black", back_color="white"):
    writer = ImageWriter()
    writer.set_options({
        'module_width': module_width,
        'module_height': module_height,
        'font_size': font_size,
        'text_distance': text_distance,
    })

    if barcode_type == 'EAN13':
        barcode = EAN13(data, writer=writer)
    elif barcode_type == 'EAN8':
        barcode = EAN8(data, writer=writer)
    elif barcode_type == 'Code128':
        barcode = Code128(data, writer=writer)
    elif barcode_type == 'Code39':
        barcode = Code39(data, writer=writer)
    elif barcode_type == 'UPCA':
        barcode = UPCA(data, writer=writer)
    elif barcode_type == 'ISBN13':
        barcode = ISBN13(data, writer=writer)
    elif barcode_type == 'ISBN10':
        barcode = ISBN10(data, writer=writer)
    elif barcode_type == 'ISSN':
        barcode = ISSN(data, writer=writer)
    elif barcode_type == 'PZN':
        barcode = PZN(data, writer=writer)
    elif barcode_type == 'JAN':
        barcode = JAN(data, writer=writer)
    elif barcode_type == 'ITF':
        barcode = ITF(data, writer=writer)
    elif barcode_type == 'GS1-128':
        barcode = Gs1_128(data, writer=writer)
    else:
        raise ValueError("Unsupported barcode type")

    barcode_bytes = BytesIO()
    barcode.write(barcode_bytes)
    barcode_bytes.seek(0)
    img = Image.open(barcode_bytes).convert("RGB")

    img = ImageOps.colorize(ImageOps.grayscale(img), black=fill_color, white=back_color)

    return img

def generate_datamatrix(data, fill_color="black", back_color="white"):
    encoded = dmtx_encode(data.encode('utf-8'))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img = ImageOps.colorize(ImageOps.grayscale(img), black=fill_color, white=back_color)
    return img

def generate_aztec(data, fill_color="black", back_color="white"):
    qr = pyqrcodeng.create(data)
    buffer = BytesIO()
    qr.png(buffer, scale=5, module_color=fill_color, background=back_color)
    img = Image.open(buffer)
    return img

def generate_pdf417(data, fill_color="black", back_color="white"):
    codes = pdf417gen.encode(data)
    img = pdf417gen.render_image(codes, scale=3, ratio=3)
    img = ImageOps.colorize(ImageOps.grayscale(img), black=fill_color, white=back_color)
    return img

def save_image(img, file_path):
    try:
        img.save(file_path)
        messagebox.showinfo("Success", f"Image saved successfully to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")

def preview_image(img):
    preview_window = tk.Toplevel(app)
    preview_window.title("Preview")
    preview_window.geometry("600x600")
    preview_canvas = tk.Canvas(preview_window, width=600, height=600)
    preview_canvas.pack()

    img.thumbnail((600, 600), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    preview_canvas.create_image(300, 300, image=tk_img)

    preview_canvas.image = tk_img
    preview_window.mainloop()

def validate_inputs(data, barcode_type, version, box_size, border, module_width, module_height, font_size, text_distance):
    if not data:
        raise ValueError("Please enter data to encode")

    if barcode_type == 'QR Code':
        if not (1 <= version <= 40):
            raise ValueError("QR Code version must be between 1 and 40")
        if box_size <= 0:
            raise ValueError("Box size must be greater than 0")
        if border < 0:
            raise ValueError("Border size cannot be negative")
    else:
        if module_width <= 0:
            raise ValueError("Module width must be greater than 0")
        if module_height <= 0:
            raise ValueError("Module height must be greater than 0")
        if font_size <= 0:
            raise ValueError("Font size must be greater than 0")
        if text_distance < 0:
            raise ValueError("Text distance cannot be negative")

def on_generate_or_preview(preview=False):
    data = data_entry.get()
    barcode_type = barcode_type_combobox.get()
    fill_color = fill_color_btn['bg']
    back_color = back_color_btn['bg']

    try:
        if barcode_type == 'QR Code':
            version = int(version_entry.get())
            error_correction = error_correction_combobox.get()
            box_size = int(box_size_entry.get())
            border = int(border_entry.get())

            error_correction_map = {
                "L": qrcode.constants.ERROR_CORRECT_L,
                "M": qrcode.constants.ERROR_CORRECT_M,
                "Q": qrcode.constants.ERROR_CORRECT_Q,
                "H": qrcode.constants.ERROR_CORRECT_H,
            }

            validate_inputs(data, barcode_type, version, box_size, border, None, None, None, None)

            img = generate_qr_code(data, version, error_correction_map[error_correction], box_size, border,
                                   fill_color=fill_color, back_color=back_color)
        elif barcode_type == 'DataMatrix':
            img = generate_datamatrix(data, fill_color=fill_color, back_color=back_color)
        elif barcode_type == 'Aztec':
            img = generate_aztec(data, fill_color=fill_color, back_color=back_color)
        elif barcode_type == 'PDF417':
            img = generate_pdf417(data, fill_color=fill_color, back_color=back_color)
        else:
            module_width = float(module_width_entry.get())
            module_height = float(module_height_entry.get())
            font_size = int(font_size_entry.get())
            text_distance = int(text_distance_entry.get())

            validate_inputs(data, barcode_type, None, None, None, module_width, module_height, font_size, text_distance)

            img = generate_barcode(data, barcode_type, module_width, module_height, font_size, text_distance, fill_color=fill_color, back_color=back_color)

        if preview:
            preview_image(img)
        else:
            output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                       filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg"),
                                                                  ("SVG files", "*.svg"), ("All files", "*.*")])
            if output_path:
                save_image(img, output_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def choose_color(btn):
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        btn.config(bg=color_code)

def on_barcode_type_change(event):
    barcode_type = barcode_type_combobox.get()
    if barcode_type == 'QR Code':
        qr_settings_frame.grid()
        barcode_settings_frame.grid_remove()
    elif barcode_type in ['EAN13', 'EAN8', 'Code128', 'Code39', 'UPCA', 'ISBN13', 'ISBN10', 'ISSN', 'PZN', 'JAN', 'ITF', 'GS1-128']:
        qr_settings_frame.grid_remove()
        barcode_settings_frame.grid()
    else:
        qr_settings_frame.grid_remove()
        barcode_settings_frame.grid_remove()

app = tk.Tk()
app.title("Enhanced QR Code & Barcode Generator")
app.geometry("900x1200")
app.configure(bg='#34495e')

window_width = 550
window_height = 500
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)
app.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

style = ttk.Style()
style.theme_use("clam")
style.configure('TFrame', background='#2c3e50')
style.configure('TButton',
                background='#2980b9',
                foreground='white',
                font=('Helvetica', 14, 'bold'),
                borderwidth=1,
                relief="raised")
style.map('TButton',
          background=[('active', '#3498db')])
style.configure('TLabel',
                background='#34495e',
                foreground='#ecf0f1',
                font=('Helvetica', 14, 'bold'))
style.configure('TEntry',
                font=('Helvetica', 14),
                padding=5)
style.configure('TCombobox',
                font=('Helvetica', 14),
                padding=5)
style.map('TCombobox',
          fieldbackground=[('readonly', '#2c3e50')],
          foreground=[('readonly', 'white')])

frame = ttk.Frame(app, padding="20", style='TFrame')
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
ttk.Label(frame, text="Select Code Type:", style='TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
barcode_type_combobox = ttk.Combobox(frame,
                                     values=["QR Code", "EAN13", "EAN8", "Code128", "Code39", "UPCA", "ISBN13", "ISBN10", "ISSN", "PZN", "JAN",
                                             "ITF", "GS1-128", "DataMatrix", "Aztec", "PDF417"], state="readonly", style='TCombobox')
barcode_type_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
barcode_type_combobox.current(0)
barcode_type_combobox.bind("<<ComboboxSelected>>", on_barcode_type_change)

ttk.Label(frame, text="Enter Data:", style='TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
data_entry = ttk.Entry(frame, width=40, style='TEntry')
data_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

qr_settings_frame = ttk.Frame(frame, style='TFrame')
qr_settings_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

ttk.Label(qr_settings_frame, text="QR Code Version (1-40):", style='TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
version_entry = ttk.Entry(qr_settings_frame, width=10, style='TEntry')
version_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
version_entry.insert(0, "1")

ttk.Label(qr_settings_frame, text="Error Correction:", style='TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
error_correction_combobox = ttk.Combobox(qr_settings_frame, values=["L", "M", "Q", "H"], state="readonly", style='TCombobox')
error_correction_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
error_correction_combobox.current(3)

ttk.Label(qr_settings_frame, text="Box Size:", style='TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
box_size_entry = ttk.Entry(qr_settings_frame, width=10, style='TEntry')
box_size_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
box_size_entry.insert(0, "10")

ttk.Label(qr_settings_frame, text="Border Size:", style='TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
border_entry = ttk.Entry(qr_settings_frame, width=10, style='TEntry')
border_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
border_entry.insert(0, "4")

barcode_settings_frame = ttk.Frame(frame, style='TFrame')
barcode_settings_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
barcode_settings_frame.grid_remove()

ttk.Label(barcode_settings_frame, text="Module Width:", style='TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
module_width_entry = ttk.Entry(barcode_settings_frame, width=10, style='TEntry')
module_width_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
module_width_entry.insert(0, "0.2")

ttk.Label(barcode_settings_frame, text="Module Height:", style='TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
module_height_entry = ttk.Entry(barcode_settings_frame, width=10, style='TEntry')
module_height_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
module_height_entry.insert(0, "15")

ttk.Label(barcode_settings_frame, text="Font Size:", style='TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
font_size_entry = ttk.Entry(barcode_settings_frame, width=10, style='TEntry')
font_size_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
font_size_entry.insert(0, "10")

ttk.Label(barcode_settings_frame, text="Text Distance:", style='TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
text_distance_entry = ttk.Entry(barcode_settings_frame, width=10, style='TEntry')
text_distance_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
text_distance_entry.insert(0, "5")

ttk.Label(frame, text="Fill Color:", style='TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
fill_color_btn = tk.Button(frame, bg="black", command=lambda: choose_color(fill_color_btn))
fill_color_btn.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

ttk.Label(frame, text="Background Color:", style='TLabel').grid(row=4, column=0, sticky=tk.W, pady=5)
back_color_btn = tk.Button(frame, bg="white", command=lambda: choose_color(back_color_btn))
back_color_btn.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)

button_frame = ttk.Frame(frame, style='TFrame')
button_frame.grid(row=12, column=0, columnspan=2, pady=10)

generate_button = ttk.Button(button_frame, text="Generate", command=lambda: on_generate_or_preview(preview=False), style='TButton')
generate_button.grid(row=0, column=0, padx=5)

preview_button = ttk.Button(button_frame, text="Preview", command=lambda: on_generate_or_preview(preview=True), style='TButton')
preview_button.grid(row=0, column=1, padx=5)

app.mainloop()