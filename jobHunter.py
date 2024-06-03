import tkinter as tk
from tkinter import PhotoImage
import indeed


def open_indeed_menu():
    root.destroy()
    indeed.indeed_menu()


def main_menu():
    global root
    root = tk.Tk()
    root.title('Job Hunter')
    root.geometry('450x550')
    #bg_image = PhotoImage(file='REPLACE.png')
    #bg_label = tk.Label(root, image=bg_image)
    #bg_label.place(relwidth=1, relheight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    # create menu text into the background image
    button_width = 11
    button_height = 4
    indeed_button = tk.Button(root, text='Indeed', font=('Helvetica', 9, 'bold'), width=button_width, height=button_height, command=open_indeed_menu)
    indeed_button.grid(row=3, column=1)
    glassdoor_button = tk.Button(root, text='Glassdoor', font=('Helvetica', 9, 'bold'), width=button_width, height=button_height, state=tk.DISABLED)
    glassdoor_button.grid(row=3, column=2)
    monster_button = tk.Button(root, text='Monster', font=('Helvetica', 9, 'bold'), width=button_width, height=button_height, state=tk.DISABLED)
    monster_button.grid(row=4, column=1)
    dice_button = tk.Button(root, text='Dice', font=('Helvetica', 9, 'bold'), width=button_width, height=button_height, state=tk.DISABLED)
    dice_button.grid(row=4, column=2)
    quit_app_button = tk.Button(root, text='Quit App', font=('Helvetica', 9, 'bold'), command=root.destroy)
    quit_app_button.grid(row=12, column=0, padx=15, pady=15)
    root.mainloop()

if __name__ == "__main__":
    main_menu()