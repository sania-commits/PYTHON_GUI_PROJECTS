from tkinter import *

first_number = second_number = operator = None

def get_digit(digit):
    current = result_label['text']
    if current == 'Error':
        current = ''
    new = current + str(digit)
    result_label.config(text=new)

def clear():
    global first_number, second_number, operator
    first_number = second_number = operator = None
    result_label.config(text="")
    history_label.config(text="")

def get_operator(op):
    global first_number,operator
    try:
        first_number = float(result_label['text'])
    except ValueError:
        result_label.config(text='Error')
        return
    operator = op
    history_label.config(text=f"{first_number} {operator}")
    result_label.config(text='')

def get_result():
    global first_number,second_number,operator

    try:
        second_number = float(result_label['text'])
    except ValueError:
        result_label.config(text='Error')
        return
    if first_number is None or operator is None:
        result_label.config(text='Error')
        return

    if operator == '+':
        answer = first_number + second_number

    elif operator == '-':
        answer = first_number - second_number

    elif operator == '*':
        answer = first_number * second_number

    else:
        if second_number ==0:
            result_label.config(text="Error")
            return
        else:
            answer = first_number / second_number

    history_label.config( text=f"{first_number} {operator} {second_number} =")
    result_label.config(text=str(int(answer)) if answer.is_integer() else str(answer))


root = Tk()
root.title('Calculator')
root.geometry('360x500')
root.minsize(320, 460)
root.configure(bg='#101b18', padx=18, pady=18)
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

Label(root, text='CALCULATOR', bg='#101b18', fg='#93a89c',
      font=('Segoe UI', 10, 'bold'), anchor='w').grid(row=0, column=0, sticky='ew', pady=(0, 14))

display = Frame(root, bg='#1c2c25', padx=16, pady=14)
display.grid(row=1, column=0, sticky='ew', pady=(0, 18))
display.columnconfigure(0, weight=1)
history_label = Label(display, text='', bg='#1c2c25', fg='#a8bcad',
                      font=('Segoe UI', 13), anchor='e')
history_label.grid(row=0, column=0, sticky='ew', pady=(0, 8))
result_label = Label(display, text='', bg='#1c2c25', fg='#f1f7f2',
                     font=('Segoe UI', 32, 'bold'), anchor='e')
result_label.grid(row=1, column=0, sticky='ew')

keypad = Frame(root, bg='#101b18')
keypad.grid(row=2, column=0, sticky='nsew')
for index in range(4):
    keypad.columnconfigure(index, weight=1, uniform='keys')
    keypad.rowconfigure(index, weight=1, uniform='keys')

keys = [('7', '8', '9', '+'), ('4', '5', '6', '-'),
        ('1', '2', '3', '*'), ('C', '0', '=', '/')]
for row, values in enumerate(keys):
    for column, text in enumerate(values):
        if text.isdigit():
            command = lambda digit=int(text): get_digit(digit)
            background, foreground = '#263b30', '#f1f7f2'
        elif text == 'C':
            command = clear
            background, foreground = '#493a2c', '#ffd5ad'
        elif text == '=':
            command = get_result
            background, foreground = '#c6ec9a', '#112622'
        else:
            command = lambda op=text: get_operator(op)
            background, foreground = '#365841', '#d9f5c6'
        button = Button(keypad, text=text, command=command,
                        bg=background, fg=foreground,
                        activebackground='#56784c', activeforeground='#ffffff',
                        font=('Segoe UI', 18, 'bold'), relief='flat', bd=0,
                        cursor='hand2', highlightthickness=0)
        button.grid(row=row, column=column, sticky='nsew',
                    padx=(0 if column == 0 else 5, 0 if column == 3 else 5),
                    pady=(0 if row == 0 else 5, 0 if row == 3 else 5))

# Keep long results inside the display when the window is resized.
def fit_display(event=None):
    width = max(display.winfo_width() - 32, 1)
    result_label.config(wraplength=width)
    history_label.config(wraplength=width)

display.bind('<Configure>', fit_display)
root.mainloop()
