import pymysql
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

# GUI Window
gui = Tk()
gui.title("Task Management System")
gui.geometry("1024x768")
tms_tree = ttk.Treeview(gui)

# functions here

# GUI contents
header = Label(gui, text="Task Management System", font=('Arial Bold', 30))
header.grid(row=0, column=0, columnspan=2, rowspan=1, padx=50, pady=40)

taskName = Label(gui, text="Task name", font=('Arial', 12))
taskName.grid(row=3, column=0, columnspan=1, padx=10, pady=5, sticky='e')
taskNameEntry = ttk.Entry(gui, width=25, font=('Arial', 12))
taskNameEntry.grid(row=3, column=1, columnspan=1, padx=5, pady=0)

taskDate = Label(gui, text="Date", font=('Arial', 12))
taskDate.grid(row=4, column=0, columnspan=1, padx=10, pady=5, sticky='e')
taskDateEntry = DateEntry(gui, selectmode='day')
taskDateEntry.grid(row=4, column=1, columnspan=1, padx=5, pady=0)

taskTime = Label(gui, text="Time", font=('Arial', 12))
taskTime.grid(row=5, column=0, columnspan=1, padx=10, pady=5, sticky='e')
taskTimeHour = ttk.Entry(gui, width=25, font=('Arial', 12))
taskTimeHour.grid(row=5, column=1, columnspan=1,padx=1, pady=0)
taskTimeAMPM = ttk.Combobox(gui, width=5,values=['AM', 'PM'])
taskTimeAMPM.grid(row=5, column=2, padx=5, pady=0)

taskPriority = Label(gui, text="Priority level", font=('Arial', 12))
taskPriority.grid(row=6, column=0, columnspan=1, padx=10, pady=5, sticky='e')
taskPriorityEntry = ttk.Combobox(gui, values=['Low', 'Medium', 'High'])
taskPriorityEntry.grid(row=6, column=1, columnspan=1, padx=5, pady=0)


addBtn = ttk.Button(gui, text='Add', width=10)
addBtn.grid(row=3, column=6, columnspan=1, rowspan=2, padx=35, pady=0)
updateBtn = ttk.Button(gui, text='Update', width=10)
updateBtn.grid(row=4, column=6, columnspan=1, rowspan=2, padx=35, pady=0)
deleteBtn = ttk.Button(gui, text='Delete', width=10)
deleteBtn.grid(row=5, column=6, columnspan=1, rowspan=2, padx=35, pady=0)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial Bold', 12))

tms_tree['columns'] = ('Priority', 'Task', 'Date', 'Time')
tms_tree.column("#0", width=0, stretch=NO)
tms_tree.column("Priority", anchor=W, width=30)
tms_tree.heading("Priority", text="Priority", anchor=W)
tms_tree.column("Task", anchor=W, width=150)
tms_tree.heading("Task", text="Task", anchor=W)
tms_tree.column("Date", anchor=W, width=70)
tms_tree.heading("Date", text="Date", anchor=W)
tms_tree.column("Time", anchor=W, width=50)
tms_tree.heading("Time", text="Time", anchor=W)


gui.mainloop()
