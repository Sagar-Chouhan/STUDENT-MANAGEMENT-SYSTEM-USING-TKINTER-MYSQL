import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def fetch_data():
    mysqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Your MySQL root password
        database="student_management"
    )
    
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT * FROM students")  # Get all data from the students table
    records = mycursor.fetchall()
    
    listBox.delete(*listBox.get_children())  # Clear the Treeview before adding new data
    
    for record in records:
        listBox.insert("", "end", values=record)
    
    mysqldb.close()

def add_student():
    student_id = e1.get()
    student_name = e2.get()
    course = e3.get()
    grade = e4.get()

    if student_id == "" or student_name == "" or course == "" or grade == "":
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return
    
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="student_management")
    mycursor = mysqldb.cursor()
    
    try:
        sql = "INSERT INTO students (student_id, student_name, course, grade) VALUES (%s, %s, %s, %s)"
        val = (student_id, student_name, course, grade)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Student added successfully!")
        fetch_data()  # Refresh the Treeview to show the new data
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Duplicate entry error code
            messagebox.showerror("Error", "Student ID already exists!")
        else:
            messagebox.showerror("Error", str(err))
        mysqldb.rollback()
    finally:
        mysqldb.close()

def update_student():
    student_id = e1.get()
    student_name = e2.get()
    course = e3.get()
    grade = e4.get()

    if student_id == "" or student_name == "" or course == "" or grade == "":
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return
    
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="student_management")
    mycursor = mysqldb.cursor()

    try:
        sql = "UPDATE students SET student_name=%s, course=%s, grade=%s WHERE student_id=%s"
        val = (student_name, course, grade, student_id)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Record updated successfully!")
        fetch_data()  # Refresh the Treeview to show the updated data
    except Exception as e:
        messagebox.showerror("Error", str(e))
        mysqldb.rollback()
    finally:
        mysqldb.close()

def delete_student():
    student_id = e1.get()

    if student_id == "":
        messagebox.showwarning("Input Error", "Please enter a Student ID.")
        return
    
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="student_management")
    mycursor = mysqldb.cursor()

    try:
        sql = "DELETE FROM students WHERE student_id=%s"
        val = (student_id,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Record deleted successfully!")
        fetch_data()  # Refresh the Treeview to show the updated data
    except Exception as e:
        messagebox.showerror("Error", str(e))
        mysqldb.rollback()
    finally:
        mysqldb.close()

def get_value(event):
    row_id = listBox.selection()[0]
    select = listBox.set(row_id)
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e1.insert(0, select['student_id'])
    e2.insert(0, select['student_name'])
    e3.insert(0, select['course'])
    e4.insert(0, select['grade'])

# GUI Setup
root = tk.Tk()
root.geometry("800x500")
root.title("Student Management System")

# Labels
tk.Label(root, text="Student Management System", fg="red", font=(None, 30)).pack(pady=20)

# Input Fields
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Student ID").grid(row=0, column=0, padx=10, pady=10)
tk.Label(frame, text="Student Name").grid(row=1, column=0, padx=10, pady=10)
tk.Label(frame, text="Course").grid(row=2, column=0, padx=10, pady=10)
tk.Label(frame, text="Grade").grid(row=3, column=0, padx=10, pady=10)

e1 = tk.Entry(frame)
e1.grid(row=0, column=1, padx=10, pady=10)
e2 = tk.Entry(frame)
e2.grid(row=1, column=1, padx=10, pady=10)
e3 = tk.Entry(frame)
e3.grid(row=2, column=1, padx=10, pady=10)
e4 = tk.Entry(frame)
e4.grid(row=3, column=1, padx=10, pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
tk.Button(button_frame, text="Add", command=add_student, height=2, width=10).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Update", command=update_student, height=2, width=10).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Delete", command=delete_student, height=2, width=10).grid(row=0, column=2, padx=10)

# Treeview for displaying records
cols = ('student_id', 'student_name', 'course', 'grade')
listBox = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    listBox.heading(col, text=col)
listBox.pack(pady=20)

listBox.bind('<Double-Button-1>', get_value)  # Bind double-click event to get selected row data

# Fetch initial data
fetch_data()  # Display data on startup

# Start the application
root.mainloop()
