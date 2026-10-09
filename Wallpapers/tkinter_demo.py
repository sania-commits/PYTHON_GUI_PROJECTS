from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def handle_login():
    email = email_input.get()
    password = password_input.get()

    if email == "demo@example.com" and password == "demo123":
        messagebox.showinfo("Demo", "Demo login successful. No account is authenticated.")
    else:
        messagebox.showinfo("Welcome", "Please enter your correct credentials")

# Create main window
root = Tk()

# Window settings
root.title("Login Form — UI Demo")
root.geometry("350x500")
root.configure(bg="#0096DC")

# Set window icon
icon = PhotoImage(file=str(BASE_DIR / "icons8-favicon-16.png"))
root.iconphoto(True, icon)

# Load and resize logo image
img = Image.open(BASE_DIR / "flipkart-logo-39904.ico")
img = img.resize((100, 100))

photo = ImageTk.PhotoImage(img)

# Display image
label = Label(root, image=photo, bg="#0096DC")
label.pack(pady=(10,10))

text_label = Label(root,text='Flipkart',fg="white",bg="#0096DC")
text_label.pack()
text_label.config(font=('verdana',24))

email_label = Label(root,text='Enter Email',fg="white",bg="#0096DC")
email_label.pack(pady=(15,5))
email_label.config(font=('verdana',14))

email_input = Entry(root, width=30)
email_input.pack(ipady= 6,pady=(1,15))

password_label = Label(root,text='Enter Password',fg="white",bg="#0096DC")
password_label.pack(pady=(15,5))
password_label.config(font=('verdana',14))

password_input = Entry(root, width=30, show='*')
password_input.pack(ipady= 6,pady=(1,15))

login_button = Button(root,text='Login Here', bg = 'white', fg = 'black', width = 10 , height=2, command=handle_login)
login_button.pack(pady=(10,5))
login_button.config(font=('verdana',12))


# Run application
root.mainloop()
