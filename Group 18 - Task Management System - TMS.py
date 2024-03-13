import pymysql
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

# Content of Functions

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


def read():
    connect = connectdb()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY PRIORITY ASC, DATE ASC, TIME ASC")
    results = cursor.fetchall()
    connect.commit()
    connect.close()
    return results


def add():
    priority = str(taskPriorityEntry.get()).strip()
    title = str(taskNameEntry.get()).strip()
    date = str(taskDateEntry.get()).strip()
    time = str(taskTimeHour.get()).strip() + ":" + str(taskTimeMin.get()).strip() + str(taskTimeAMPM.get()).strip()

    year = int(date[-2:])

    try:
        int(taskTimeHour.get())
        int(taskTimeHour.get())
    except ValueError:
        messagebox.showinfo("Error", "Time value must be a number")
        return
    if ((priority == '') or (title == '')
            or (date == '') or (time == '')):
        messagebox.showinfo("Error", "Task name cannot be blank")
        return
    elif ((len(taskTimeHour.get()) != 2 or len(taskTimeMin.get()) != 2 or
          int(taskTimeHour.get()) > 12) or int(taskTimeMin.get()) > 12 or
          int(taskTimeHour.get()) < 0 or int(taskTimeMin.get()) < 0):
        messagebox.showinfo("Error", "Incorrect time value")
        return

    else:
        if year < 24:
            date += ' (OVERDUE)'
            print(date)
        try:
            connect = connectdb()
            cursor = connect.cursor()
            cursor.execute("INSERT INTO tasks VALUES ('"+priority+"', '"+title+"', '"+date+"', '"+time+"')")
            connect.commit()
            connect.close()
        except pymysql.err.IntegrityError:
            messagebox.showinfo("Error", "Task name already exists")
            return

    table_refresh()


def update():
    selectedTask = ''
    decision = messagebox.askquestion("Confirmation", "Update selected task?")

    if decision != 'yes':
        return
    else:
        try:
            selectedItem = tms_tree.selection()[0]
            selectedTask = str(tms_tree.item(selectedItem)['values'][1])
        except ValueError:
            messagebox.showinfo("Error", "No task selected")

        priority = str(taskPriorityEntry.get())
        title = str(taskNameEntry.get())
        date = str(taskDateEntry.get())
        time = str(taskTimeHour.get()) + ":" + str(taskTimeMin.get()) + str(taskTimeAMPM.get())

        if ((priority.strip() == '') or (title.strip() == '')
                or (date.strip() == '') or (time.strip() == '')):
            messagebox.showinfo("Error", "Task name cannot be blank")
            return
        else:
            try:
                conn = connectdb()
                cursor = conn.cursor()
                cursor.execute("UPDATE tasks SET PRIORITY='"+priority+"', TITLE='"+title+"', DATE='"+date+"', TIME='"+time+"' WHERE TITLE='"+selectedTask+"' ")
                conn.commit()
                conn.close()
            except ValueError:
                messagebox.showinfo("Error", "Something happened omg")
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
            messagebox.showinfo("Error", "Delete failed")
            return

    table_refresh()


def select(event):
    region = tms_tree.identify("region", event.x, event.y)
    if region == "nothing":
        table_refresh()
    elif region == "heading":
        return
    else:
        try:
            selectedItem = tms_tree.selection()[0]
            priority = str(tms_tree.item(selectedItem)['values'][0])
            title = str(tms_tree.item(selectedItem)['values'][1])
            date = str(tms_tree.item(selectedItem)['values'][2])
            time = str(tms_tree.item(selectedItem)['values'][3])

            taskPriorityVar.set(priority)
            taskNameVar.set(title)
            taskDateVar.set(date)
            if time[1] == ':':
                taskTimeVar1.set(time[0])
                taskTimeVar2.set(time[2:4])
            else:
                taskTimeVar1.set(time[:2])
                taskTimeVar2.set(time[3:5])
            taskTimeVar3.set(time[-2:])
        except ValueError:
            messagebox.showinfo("Error", "Idk")


# GUI contents

# GUI Window
gui = Tk()
gui.title("Task Management System")
gui.geometry("1024x768")

# Frames
headerFrame = tk.Frame(gui)
nameFrame = tk.Frame(gui)
dateFrame = tk.Frame(gui)
timeFrame = tk.Frame(gui)
priorityFrame = tk.Frame(gui)
buttonFrame = tk.Frame(gui)
treeFrame = tk.Frame(gui)

headerFrame.pack(side='top', pady=40)
nameFrame.pack(pady=10)
dateFrame.pack(pady=10)
timeFrame.pack(pady=10)
priorityFrame.pack(pady=10)
buttonFrame.pack(pady=10)
treeFrame.pack(pady=10)

header = Label(headerFrame, text="Task Management System", font=('Arial Bold', 30))
header.pack()

taskName = Label(nameFrame, text="Task name: ", font=('Arial', 12))
taskName.pack(side='left')
taskNameVar = tk.StringVar()
taskNameEntry = ttk.Entry(nameFrame, width=25, font=('Arial', 12), textvariable=taskNameVar)
taskNameEntry.pack(side='right')

taskDate = Label(dateFrame, text="Date: ", font=('Arial', 12))
taskDate.pack(side='left')
taskDateVar = tk.StringVar()
taskDateEntry = DateEntry(dateFrame, selectmode='day', textvariable=taskDateVar)
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
taskTimeMin = ttk.Spinbox(timeFrame, from_=00, to=59, format="%02.0f", textvariable=taskTimeVar2, width=3)
taskTimeMin.pack(side='left')
taskTimeVar3 = tk.StringVar()
taskTimeVar3.set("PM")
taskTimeAMPM = ttk.Combobox(timeFrame, values=['AM', 'PM'], textvariable=taskTimeVar3, width=3)
taskTimeAMPM.pack(side='left', padx=5)

taskPriority = Label(priorityFrame, text="Priority level: ", font=('Arial', 12))
taskPriority.pack(side='left')
taskPriorityVar = tk.StringVar()
taskPriorityVar.set("2 - Normal")
taskPriorityEntry = ttk.Combobox(priorityFrame, values=['1 - High', '2 - Normal', '3 - Low'],
                                 textvariable=taskPriorityVar)
taskPriorityEntry.pack(side='left')

addBtn = ttk.Button(buttonFrame, text='Add', width=10, command=add)
addBtn.pack(side='left')
updateBtn = ttk.Button(buttonFrame, text='Update', width=10, command=update)
updateBtn.pack(side='left')
deleteBtn = ttk.Button(buttonFrame, text='Delete', width=10, command=delete)
deleteBtn.pack(side='left')

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial Bold', 12))

tms_tree = ttk.Treeview(treeFrame, selectmode='browse')
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
tms_tree.pack(side='left')

scrollBar = ttk.Scrollbar(treeFrame, orient='vertical', command=tms_tree.yview)
scrollBar.pack(side='right', fill='y', expand=True)
tms_tree.configure(yscrollcommand=scrollBar.set)

tms_tree.bind("<Double-1>", select)

table_refresh()

gui.mainloop()
