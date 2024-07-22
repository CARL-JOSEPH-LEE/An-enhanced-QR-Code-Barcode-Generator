_V='PDF417'
_U='DataMatrix'
_T='Preview'
_S='#2c3e50'
_R='JAN'
_Q='PZN'
_P='ISBN13'
_O='UPCA'
_N='Code39'
_M='Code128'
_L='RGB'
_K='readonly'
_J='TCombobox'
_I='Helvetica'
_H='TButton'
_G='QR Code'
_F='EAN13'
_E='TFrame'
_D='black'
_C='white'
_B='TEntry'
_A='TLabel'
import tkinter as tk
from tkinter import ttk,filedialog,messagebox,colorchooser
import qrcode
from barcode import EAN13,Code128,Code39,UPCA,ISBN13,PZN,JAN
from barcode.writer import ImageWriter
from pylibdmtx.pylibdmtx import encode as dmtx_encode
from PIL import Image,ImageTk,ImageDraw,ImageOps
from io import BytesIO
import pdf417gen,pyqrcodeng
def generate_qr_code(data,version,error_correction,box_size,border,fill_color=_D,back_color=_C):A=qrcode.QRCode(version=version,error_correction=error_correction,box_size=box_size,border=border);A.add_data(data);A.make(fit=True);B=A.make_image(fill_color=fill_color,back_color=back_color).convert(_L);return B
def generate_barcode(data,barcode_type=_F,module_width=.2,module_height=15,font_size=10,text_distance=5,fill_color=_D,back_color=_C):
	B=barcode_type;C=data;A=ImageWriter();A.set_options({'module_width':module_width,'module_height':module_height,'font_size':font_size,'text_distance':text_distance})
	if B==_F:D=EAN13(C,writer=A)
	elif B==_M:D=Code128(C,writer=A)
	elif B==_N:D=Code39(C,writer=A)
	elif B==_O:D=UPCA(C,writer=A)
	elif B==_P:D=ISBN13(C,writer=A)
	elif B==_Q:D=PZN(C,writer=A)
	elif B==_R:D=JAN(C,writer=A)
	else:raise ValueError('Unsupported barcode type')
	E=BytesIO();D.write(E);E.seek(0);F=Image.open(E).convert(_L);F=ImageOps.colorize(ImageOps.grayscale(F),black=fill_color,white=back_color);return F
def generate_datamatrix(data,fill_color=_D,back_color=_C):A=dmtx_encode(data.encode('utf-8'));B=Image.frombytes(_L,(A.width,A.height),A.pixels);B=ImageOps.colorize(ImageOps.grayscale(B),black=fill_color,white=back_color);return B
def generate_aztec(data,fill_color=_D,back_color=_C):B=pyqrcodeng.create(data);A=BytesIO();B.png(A,scale=5,module_color=fill_color,background=back_color);C=Image.open(A);return C
def generate_pdf417(data,fill_color=_D,back_color=_C):B=pdf417gen.encode(data);A=pdf417gen.render_image(B,scale=3,ratio=3);A=ImageOps.colorize(ImageOps.grayscale(A),black=fill_color,white=back_color);return A
def save_image(img,file_path):
	A=file_path
	try:img.save(A);messagebox.showinfo('Success',f"Image saved successfully to {A}")
	except Exception as B:messagebox.showerror('Error',f"Failed to save image: {B}")
def preview_image(img):A=tk.Toplevel(app);A.title(_T);A.geometry('600x600');B=tk.Canvas(A,width=600,height=600);B.pack();img.thumbnail((600,600),Image.LANCZOS);C=ImageTk.PhotoImage(img);B.create_image(300,300,image=C);B.image=C;A.mainloop()
def validate_inputs(data,barcode_type,version,box_size,border,module_width,module_height,font_size,text_distance):
	if not data:raise ValueError('Please enter data to encode')
	if barcode_type==_G:
		if not 1<=version<=40:raise ValueError('QR Code version must be between 1 and 40')
		if box_size<=0:raise ValueError('Box size must be greater than 0')
		if border<0:raise ValueError('Border size cannot be negative')
	else:
		if module_width<=0:raise ValueError('Module width must be greater than 0')
		if module_height<=0:raise ValueError('Module height must be greater than 0')
		if font_size<=0:raise ValueError('Font size must be greater than 0')
		if text_distance<0:raise ValueError('Text distance cannot be negative')
def on_generate_or_preview(preview=False):
	A=None;B=data_entry.get();C=barcode_type_combobox.get();E=fill_color_btn['bg'];F=back_color_btn['bg']
	try:
		if C==_G:G=int(version_entry.get());O=error_correction_combobox.get();H=int(box_size_entry.get());I=int(border_entry.get());P={'L':qrcode.constants.ERROR_CORRECT_L,'M':qrcode.constants.ERROR_CORRECT_M,'Q':qrcode.constants.ERROR_CORRECT_Q,'H':qrcode.constants.ERROR_CORRECT_H};validate_inputs(B,C,G,H,I,A,A,A,A);D=generate_qr_code(B,G,P[O],H,I,fill_color=E,back_color=F)
		elif C==_U:D=generate_datamatrix(B,fill_color=E,back_color=F)
		elif C=='Aztec':D=generate_aztec(B,fill_color=E,back_color=F)
		elif C==_V:D=generate_pdf417(B,fill_color=E,back_color=F)
		else:J=float(module_width_entry.get());K=float(module_height_entry.get());L=int(font_size_entry.get());M=int(text_distance_entry.get());validate_inputs(B,C,A,A,A,J,K,L,M);D=generate_barcode(B,C,J,K,L,M,fill_color=E,back_color=F)
		if preview:preview_image(D)
		else:
			N=filedialog.asksaveasfilename(defaultextension='.png',filetypes=[('PNG files','*.png'),('JPG files','*.jpg'),('SVG files','*.svg'),('All files','*.*')])
			if N:save_image(D,N)
	except Exception as Q:messagebox.showerror('Error',f"An error occurred: {Q}")
def choose_color(btn):
	A=colorchooser.askcolor(title='Choose color')[1]
	if A:btn.config(bg=A)
def on_barcode_type_change(event):
	A=barcode_type_combobox.get()
	if A==_G:qr_settings_frame.grid();barcode_settings_frame.grid_remove()
	elif A in[_F,_M,_N,_O,_P,_Q,_R]:qr_settings_frame.grid_remove();barcode_settings_frame.grid()
	else:qr_settings_frame.grid_remove();barcode_settings_frame.grid_remove()
app=tk.Tk()
app.title('Enhanced QR Code & Barcode Generator')
app.geometry('800x1000')
app.configure(bg=_S)
window_width=800
window_height=1000
screen_width=app.winfo_screenwidth()
screen_height=app.winfo_screenheight()
position_top=int(screen_height/2-window_height/2)
position_right=int(screen_width/2-window_width/2)
app.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
style=ttk.Style()
style.theme_use('clam')
style.configure(_E,background=_S)
style.configure(_H,background='#e74c3c',foreground=_C,font=(_I,12,'bold'))
style.map(_H,background=[('active','#d35400')])
style.configure(_A,background=_S,foreground='#ecf0f1',font=(_I,12,'bold'))
style.configure(_B,font=(_I,12))
style.configure(_J,font=(_I,12))
style.map(_J,fieldbackground=[(_K,'#34495e')],foreground=[(_K,_C)])
frame=ttk.Frame(app,padding='20',style=_E)
frame.grid(row=0,column=0,sticky=(tk.W,tk.E,tk.N,tk.S))
ttk.Label(frame,text='Select Code Type:',style=_A).grid(row=0,column=0,sticky=tk.W,pady=5)
barcode_type_combobox=ttk.Combobox(frame,values=[_G,_F,_M,_N,_O,_P,_Q,_R,_U,'Aztec',_V],state=_K,style=_J)
barcode_type_combobox.grid(row=0,column=1,sticky=(tk.W,tk.E),pady=5)
barcode_type_combobox.current(0)
barcode_type_combobox.bind('<<ComboboxSelected>>',on_barcode_type_change)
ttk.Label(frame,text='Enter Data:',style=_A).grid(row=1,column=0,sticky=tk.W,pady=5)
data_entry=ttk.Entry(frame,width=40,style=_B)
data_entry.grid(row=1,column=1,sticky=(tk.W,tk.E),pady=5)
qr_settings_frame=ttk.Frame(frame,style=_E)
qr_settings_frame.grid(row=2,column=0,columnspan=2,pady=10,sticky=(tk.W,tk.E))
ttk.Label(qr_settings_frame,text='QR Code Version (1-40):',style=_A).grid(row=0,column=0,sticky=tk.W,pady=5)
version_entry=ttk.Entry(qr_settings_frame,width=10,style=_B)
version_entry.grid(row=0,column=1,sticky=(tk.W,tk.E),pady=5)
version_entry.insert(0,'1')
ttk.Label(qr_settings_frame,text='Error Correction:',style=_A).grid(row=1,column=0,sticky=tk.W,pady=5)
error_correction_combobox=ttk.Combobox(qr_settings_frame,values=['L','M','Q','H'],state=_K,style=_J)
error_correction_combobox.grid(row=1,column=1,sticky=(tk.W,tk.E),pady=5)
error_correction_combobox.current(3)
ttk.Label(qr_settings_frame,text='Box Size:',style=_A).grid(row=2,column=0,sticky=tk.W,pady=5)
box_size_entry=ttk.Entry(qr_settings_frame,width=10,style=_B)
box_size_entry.grid(row=2,column=1,sticky=(tk.W,tk.E),pady=5)
box_size_entry.insert(0,'10')
ttk.Label(qr_settings_frame,text='Border Size:',style=_A).grid(row=3,column=0,sticky=tk.W,pady=5)
border_entry=ttk.Entry(qr_settings_frame,width=10,style=_B)
border_entry.grid(row=3,column=1,sticky=(tk.W,tk.E),pady=5)
border_entry.insert(0,'4')
barcode_settings_frame=ttk.Frame(frame,style=_E)
barcode_settings_frame.grid(row=2,column=0,columnspan=2,pady=10,sticky=(tk.W,tk.E))
barcode_settings_frame.grid_remove()
ttk.Label(barcode_settings_frame,text='Module Width:',style=_A).grid(row=0,column=0,sticky=tk.W,pady=5)
module_width_entry=ttk.Entry(barcode_settings_frame,width=10,style=_B)
module_width_entry.grid(row=0,column=1,sticky=(tk.W,tk.E),pady=5)
module_width_entry.insert(0,'0.2')
ttk.Label(barcode_settings_frame,text='Module Height:',style=_A).grid(row=1,column=0,sticky=tk.W,pady=5)
module_height_entry=ttk.Entry(barcode_settings_frame,width=10,style=_B)
module_height_entry.grid(row=1,column=1,sticky=(tk.W,tk.E),pady=5)
module_height_entry.insert(0,'15')
ttk.Label(barcode_settings_frame,text='Font Size:',style=_A).grid(row=2,column=0,sticky=tk.W,pady=5)
font_size_entry=ttk.Entry(barcode_settings_frame,width=10,style=_B)
font_size_entry.grid(row=2,column=1,sticky=(tk.W,tk.E),pady=5)
font_size_entry.insert(0,'10')
ttk.Label(barcode_settings_frame,text='Text Distance:',style=_A).grid(row=3,column=0,sticky=tk.W,pady=5)
text_distance_entry=ttk.Entry(barcode_settings_frame,width=10,style=_B)
text_distance_entry.grid(row=3,column=1,sticky=(tk.W,tk.E),pady=5)
text_distance_entry.insert(0,'5')
ttk.Label(frame,text='Fill Color:',style=_A).grid(row=3,column=0,sticky=tk.W,pady=5)
fill_color_btn=tk.Button(frame,bg=_D,command=lambda:choose_color(fill_color_btn))
fill_color_btn.grid(row=3,column=1,sticky=(tk.W,tk.E),pady=5)
ttk.Label(frame,text='Background Color:',style=_A).grid(row=4,column=0,sticky=tk.W,pady=5)
back_color_btn=tk.Button(frame,bg=_C,command=lambda:choose_color(back_color_btn))
back_color_btn.grid(row=4,column=1,sticky=(tk.W,tk.E),pady=5)
button_frame=ttk.Frame(frame,style=_E)
button_frame.grid(row=12,column=0,columnspan=2,pady=10)
generate_button=ttk.Button(button_frame,text='Generate',command=lambda:on_generate_or_preview(preview=False),style=_H)
generate_button.grid(row=0,column=0,padx=5)
preview_button=ttk.Button(button_frame,text=_T,command=lambda:on_generate_or_preview(preview=True),style=_H)
preview_button.grid(row=0,column=1,padx=5)
app.mainloop()