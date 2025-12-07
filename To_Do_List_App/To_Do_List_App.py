

import sqlite3
# Connect to database (creates if not exists
conn = sqlite3.connect("tasks.db")
#create cursor
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT NOT NULL
)
""")


conn.commit()
conn.close()

#Add task function
def add_task(task_name):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    #add task
    cursor.execute("INSERT INTO tasks(task, status) VALUES(?, ?)",(task_name,"pending"))
    conn.commit()
    conn.close()
    print(f"Task '{task_name}' added successfully!")

def view_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    #view tasks
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    if len(rows) == 0:
        print("TO-DO List is empty")
    else:
        for row in rows:
            print(f"ID: {row[0]} | Task_Name: {row[1]} | Status: {row[2]}")

def mark_done(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    #update task status
    cursor.execute("UPDATE tasks SET status='done' WHERE id = ?",(task_id,))
    if cursor.rowcount == 0:
        print(f"No task with ID {task_id} found.")
    else:
        print(f"Task {task_id} marked as done.")
    conn.commit()
    conn.close()         

def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    #delete task
    cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
    if cursor.rowcount == 0:
        print(f"No task with ID {task_id} found.")
    else:
        print(f"Task {task_id} deleted.")
    conn.commit()
    conn.close()


import json
def backup_to_json():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    #view tasks
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    
    tasks_list = [{"id": t[0], "task": t[1], "status": t[2]} for t in tasks]

    with open("tasks_backup.json","w") as file:
        json.dump(tasks_list, file, indent=4)

    print("Tasks backed up to tasks_backup.json")
        

def restore_from_json():
    try:
        with open("tasks_backup.json", "r") as f:
            tasks_list = json.load(f)
    except FileNotFoundError:
        print("Backup file not found.")
        return
    
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    for t in tasks_list:
        cursor.execute(
            "INSERT OR IGNORE INTO tasks (id, task, status) VALUES (?, ?, ?)",
            (t["id"], t["task"], t["status"])
        )
    conn.commit()
    conn.close()
    print("Tasks restored from tasks_backup.json")


def menu():
    while True:
        print("=======TO-DO List Menu=======")
        print("1. Add Tasks")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Backup Tasks to JSON")
        print("6. Restore Tasks from JSON")
        print("7 Exit")

        choice = input("Enter your choice: ")

        match (choice):
            case "1": 
                task_name = input("Enter task name:")
                add_task(task_name)
            case "2": 
                view_tasks()    
            case "3": 
                task_id = int(input("Enter task ID to mark sd done: "))
                mark_done(task_id) 
            case "4": 
                task_id = int(input("Enter task ID to delete: "))
                delete_task(task_id)     
            case "5": 
                backup_to_json()   
            case "6": 
                restore_from_json() 
            case "7":
                break
            case _:
                print("Invalid choice")        
if __name__ == "__main__":
    menu()