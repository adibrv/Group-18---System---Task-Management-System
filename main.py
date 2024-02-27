import pymysql
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

# Connect to DB


def connectdb():
    connect = pymysql.connect(
        host='localhost', user='root', password='', db='tasklist'
    )
    return connect


def table_refresh():
    for data in tms_tree.get_children():
        tms_tree.delete(data)

    for array in read():
        tms_tree.insert(parent='', index='end', iid=array, text="", values=array, tag='row')

    tms_tree.tag_configure('row', background='#EEEEEE', font=('Arial', 12))
    tms_tree.pack()


# GUI Window
gui = Tk()
gui.title("Task Management System")
gui.geometry("1024x768")
tms_tree = ttk.Treeview(gui)

# functions content


def read():
    connect = connectdb()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM tasks")
    results = cursor.fetchall()
    connect.commit()
    connect.close()
    return results


def add():
    priority = str(taskPriorityEntry.get())
    title = str(taskNameEntry.get())
    date = str(taskDateEntry.get())
    time = str(taskTimeHour.get()) + ":" + str(taskTimeMin.get()) + str(taskTimeAMPM.get())

    if ((priority == '' or priority == ' ') or (title == '' or title == ' ')
            or (date == '' or date == ' ') or (time == '' or time == ' ')):
        messagebox.showinfo("Error", "One or more entries are blank")
        return
    else:
        try:
            connect = connectdb()
            cursor = connect.cursor()
            cursor.execute("INSERT INTO tasks VALUES ('"+priority+"', '"+title+"', '"+date+"', '"+time+"')")
            connect.commit()
            connect.close()
        except:
            messagebox.showinfo("Error", "Task name already exists")
            return

    table_refresh()


def delete():
    decision = messagebox.askquestion("Confirmation", "Delete selected task?")
    if decision != "yes":
        return
    else:
        selectedItem = tms_tree.selection()[0]
        deleteTask = str(tms_tree.item(selectedItem)['values'][1])
        try:
            conn = connectdb()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE TITLE='"+str(deleteTask)+"'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "IDK")
            return

    table_refresh()


# GUI contents

# Frames
headerFrame = tk.Frame(gui)
nameFrame = tk.Frame(gui)
dateFrame = tk.Frame(gui)
timeFrame = tk.Frame(gui)
priorityFrame = tk.Frame(gui)
buttonFrame = tk.Frame(gui)

headerFrame.pack(side='top', pady=40)
nameFrame.pack(pady=10)
dateFrame.pack(pady=10)
timeFrame.pack(pady=10)
priorityFrame.pack(pady=10)
buttonFrame.pack(pady=10)

header = Label(headerFrame, text="Task Management System", font=('Arial Bold', 30))
header.pack()

taskName = Label(nameFrame, text="Task name: ", font=('Arial', 12))
taskName.pack(side='left')
taskNameEntry = ttk.Entry(nameFrame, width=25, font=('Arial', 12))
taskNameEntry.pack(side='right')

taskDate = Label(dateFrame, text="Date: ", font=('Arial', 12))
taskDate.pack(side='left')
taskDateEntry = DateEntry(dateFrame,selectmode='day')
taskDateEntry.pack(side='right')

taskTime = Label(timeFrame, text="Time: ", font=('Arial', 12))
taskTime.pack(side='left')
taskTimeVar1 = tk.StringVar()
taskTimeVar1.set("12")
taskTimeHour = ttk.Spinbox(timeFrame, from_=1, to=12, textvariable=taskTimeVar1, width=3)
taskTimeHour.pack(side='left')
taskTimeVar2 = tk.StringVar()
taskTimeVar2.set("00")
taskTime2 = Label(timeFrame, text=":", font=('Arial', 12))
taskTime2.pack(side='left')
taskTimeMin = ttk.Spinbox(timeFrame, from_=00, to=59, textvariable=taskTimeVar2, width=3)
taskTimeMin.pack(side='left')
taskTimeVar3 = tk.StringVar()
taskTimeVar3.set("PM")
taskTimeAMPM = ttk.Combobox(timeFrame, values=['AM', 'PM'], textvariable=taskTimeVar3, width=3)
taskTimeAMPM.pack(side='left', padx=5)

taskPriority = Label(priorityFrame, text="Priority level: ", font=('Arial', 12))
taskPriority.pack(side='left')
taskPriorityVar = tk.StringVar()
taskPriorityVar.set("Medium")
taskPriorityEntry = ttk.Combobox(priorityFrame, values=['Low', 'Medium', 'High'], textvariable=taskPriorityVar)
taskPriorityEntry.pack(side='left')

addBtn = ttk.Button(buttonFrame, text='Add', width=10, command=add)
addBtn.pack(side='left')
updateBtn = ttk.Button(buttonFrame, text='Update', width=10)
updateBtn.pack(side='left')
deleteBtn = ttk.Button(buttonFrame, text='Delete', width=10, command=delete)
deleteBtn.pack(side='left')

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial Bold', 12))

tms_tree['columns'] = ('Priority', 'Task', 'Date', 'Time')
tms_tree.column("#0", width=0, stretch=NO)
tms_tree.column("Priority", anchor=W, width=150)
tms_tree.heading("Priority", text="Priority", anchor=W)
tms_tree.column("Task", anchor=W, width=350)
tms_tree.heading("Task", text="Task", anchor=W)
tms_tree.column("Date", anchor=W, width=170)
tms_tree.heading("Date", text="Date", anchor=W)
tms_tree.column("Time", anchor=W, width=150)
tms_tree.heading("Time", text="Time", anchor=W)
tms_tree.pack()
table_refresh()

gui.mainloop()
