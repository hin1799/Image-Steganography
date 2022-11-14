from tkinter import *
from tkinter import messagebox as mb
import tkinter.filedialog
from PIL import ImageTk
from PIL import Image
from io import BytesIO
import os

img_size=0

def encode_img_frame1(F):
    F.destroy()
    F1 = Frame(root)
    label1 = Label(F1,text="Select image in which you want to hide text:")
    label1.config(font=('Times New Roman',16,'bold'),bg='#f0f0f0')
    label1.grid()

    btn_select = Button(F1, text="Choose Image", command=lambda: encode_img_frame2(F1))
    btn_select.config(font=('Helvetica',14), bg='#153462',fg="white")
    btn_select.grid()

    btn_cancel =  Button(F1, text="Cancel", command=lambda: back_screen(F1))
    btn_cancel.config(font=('Helvetica',14), bg='#EC2525',fg="white")
    btn_cancel.grid(pady=15)
    btn_cancel.grid()
    F1.grid()


def encode_img_frame2(F):
    F2 = Frame(root)
    imgfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg'),('All Files', '*.*')]))

    if not imgfile:
        mb.showerror("Error","You have not selected any file!")
    else:
        my_img = Image.open(imgfile)
        new_img = my_img.resize((300,200))
        img = ImageTk.PhotoImage(new_img)

        label1 = Label(F2,text="Selected Image")
        label1.config(font=('Helvetica',14,'bold'))
        label1.grid()

        board = Label(F2,image=img)
        board.image = img
        global img_size 
        img_size = os.stat(imgfile)
        global img_width
        global img_height
        img_width, img_height = my_img.size
        board.grid()

        label2 = Label(F2,text="Enter secret message")
        label2.config(font=('Helvetica',14,'bold'))
        label2.grid(pady=15)
 
        textbox = Text(F2, width=50, height=10)
        textbox.grid()

        btn_encode = Button(F2,text="Encode Image", command= lambda:[encoding(textbox,my_img), back_screen(F2)], padx=14, bg="#153462", fg="white")
        btn_encode.config(font=('Helvetica',14), bg='#153462')
        #data = textbox.get("1.0", "end-1c")
        btn_cancel =  Button(F2, text="Cancel", command=lambda: back_screen(F2))
        btn_cancel.config(font=('Helvetica',14), bg='#EC2525',fg="white")
        btn_encode.grid(pady=15)
        btn_encode.grid()
        btn_cancel.grid()

        F2.grid(row=1)
        F.destroy()


def encoding(text, img):
    data = text.get("1.0", "end-1c")
    if(len(data) == 0):
        mb.showinfo("Alert", "Please enter text in textbox!")
    else:
        new_img = img.copy()
        encode_text(new_img,data)
        new_file = BytesIO()
        temp=os.path.splitext(os.path.basename(img.filename))[0]
        new_img.save(tkinter.filedialog.asksaveasfilename(initialfile=temp,filetypes=([('png','*.png')]), defaultextension=".png"))

        global d_img_size, d_img_width, d_img_height
        d_img_size = new_file.tell()
        d_img_width, d_img_height = new_img.size

        mb.showinfo("Success","Encoding is successful!\n File saved")

def encode_text(new_img, data):
    w = new_img.size[0]
    (x,y) = (0,0)

    for pixel in modify_pixels(new_img.getdata(), data):
        new_img.putpixel((x,y), pixel)
        if(x == w-1):
            x = 0
            y += 1
        else:
            x += 1

#function to generate data
def generate_data(data):
    new_data = []

    for i in data:
        new_data.append(format(ord(i),'08b'))
    return new_data


def modify_pixels(pix, data):
    data_list = generate_data(data)
    data_len = len(data_list)
    img_data = iter(pix)

    for i in range(data_len):
        #Extract 3 pixels at one time
        pix = [v for v in img_data.__next__()[:3] + img_data.__next__()[:3] + img_data.__next__()[:3]]

        for j in range(0,8):
            if(data_list[i][j] == '0') and (pix[j]%2 != 0):
                pix[j] -= 1
            
            elif(data_list[i][j] == 1) and (pix[j]%2 == 0):
                pix[j] -= 1
        
        if(i == data_len - 1):
            if(pix[-1]%2 == 0):
                pix[-1] -= 1
        
        else:
            if(pix[-1]%2 != 0):
                pix[-1] -= 1
        
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def decode_img_frame1(F):
    F.destroy()
    F1 = Frame(root)
    label1 = Label(F1, text="Select the image with hidden text")
    label1.config(font=('Times New Roman', 16, 'bold'))
    label1.grid()
    label1.config(bg='#f0f0f0', fg='#153462')

    btn_select = Button(F1, text="Choose Image", command=lambda: decode_img_frame2(F1))
    btn_select.config(font=('Helvetica',14), bg='#153462',fg="white")
    btn_select.grid()

    btn_cancel =  Button(F1, text="Cancel", command=lambda: back_screen(F1))
    btn_cancel.config(font=('Helvetica',14), bg='#EC2525',fg="white")
    btn_cancel.grid(pady=15)
    btn_cancel.grid()
    F1.grid()



def decode_img_frame2(F):
    F2 = Frame(root)
    imgfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg'),('All Files', '*.*')]))

    if not imgfile:
        mb.showerror("Error","You have not selected any file!")
    else:
        my_img = Image.open(imgfile, 'r')
        my_image = my_img.resize((300,200))
        img = ImageTk.PhotoImage(my_image)

        label1 = Label(F2, text="Selected image:")
        label1.config(font=('Helvetica',14,'bold'))
        label1.grid()

        board = Label(F2, image=img)
        board.image = img
        board.grid()

        hidden_text = decode(my_img)
        label2 = Label(F2, text='Hidden text is:')
        label2.config(font=('Helvetica', 14, 'bold'))
        label2.grid(pady=10)

        textbox = Text(F2, width=50, height=10)
        textbox.insert(INSERT, hidden_text)
        textbox.configure(state='disabled') #Disabling the textbox which displays hidden text
        textbox.grid()

        btn_cancel =  Button(F2, text="Cancel", command=lambda: back_screen(F2))
        btn_cancel.config(font=('Helvetica',14), bg='#EC2525',fg="white")
        btn_cancel.grid()

        F2.grid(row=1)
        F.destroy()


def decode(image):
    image_data = iter(image.getdata())
    data = ''

    while(True):
        pixels = [value for value in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]

        str = ''
        for i in pixels[:8]:
            if i % 2 == 0:
                str += '0'
            else:
                str += '1'

        data += chr(int(str, 2))
        if pixels[-1] % 2 !=0:
            return data
             


#Function for main gui frame
def main_frame(root):
    root.title('Image Steganography')
    root.geometry('500x600')
    root.resizable(width=False, height=False)
    root.config(bg='#f0f0f0')
    frame = Frame(root)
    frame.grid()

    title = Label(frame,text="Image Steganography",fg='#153462')
    title.config(font=('Times new roman',25,'bold'))
    title.grid(pady=10)
    title.config(bg='#f0f0f0')
    title.grid(row=1)

    encode = Button(frame,text="Encode Image", command= lambda:encode_img_frame1(frame), padx=14, bg="#153462", fg="white")
    encode.config(font=('Helvetica',14), bg='#153462')
    encode.grid(row=2)

    decode = Button(frame,text="Decode Image", command= lambda: decode_img_frame1(frame), padx=14, bg="#153462", fg='white')
    decode.config(font=('Helvetica',14), bg='#153462')
    decode.grid(pady=12)
    decode.grid(row=3) 

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)


#function to go back to main screen
def back_screen(frame):
    frame.destroy()
    main_frame(root)


root=Tk()
main_frame(root)
root.mainloop()