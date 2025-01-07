import sqlite3

connection = sqlite3.connect("todo_list.db") #Anslut till databas todo_list.db

cur = connection.cursor()  # Skapar ett cursor-objekt som används för att köra SQL-kommandon och hämta resultat


# Skapa tabellen Todolist om den inte redan finns
cur.execute('''
    CREATE TABLE IF NOT EXISTS Todolist ( -- skapar en tabell om den inte finns
        id INTEGER PRIMARY KEY, -- Unikt ID för varje uppgift
        description TEXT NOT NULL, -- Beskrivning av uppgiften (obligatorisk)
        date TEXT, -- Datum för uppgiften
        time TEXT, -- Tid för uppgiften
        status INT -- Status på uppgiften (klar eller inte klar)
    ) 
''') 


while True: #Skapa en loop för menyn man skall lägga tasks ta  bort etc
    print("\nMenu: ")
    print("1. Add task")
    print("2. Show all tasks")
    print("3. Change task status")
    print("4. Delete task")
    print("5. Quit")
    
    choice = (input("Choose alternative: "))
    
    if choice == "1":
            print("Enter task in the following format:")
            print("description, date(YYYY-MM-DD), time(HH:MM), status(0 = not completed, 1 = completed)")
            user_input = input("Your input: ")

            # Dela upp inputen i fyra delar
            description, date, time, status = user_input.split(",") #splitta vår input så vi delar upp info

            status = int(status)


            print(f"Description: {description}")
            print(f"Date: {date}")
            print(f"Time: {time}")
            print(f"Status: {status}")


            cur.execute(f"""INSERT INTO Todolist -- Lägger till en ny uppgift i tabellen Todolist
                                    (description, date, time, status) -- Specifierar kolumnerna där värden ska läggas in
                                    VALUES ('{description}', '{date}', '{time}', {status})-- Använder variabler från användarens input""")  
            # Spara ändringen i databasen
            connection.commit()

            print("Task added successfully!")

    elif choice == "2":
        cur.execute("SELECT * FROM todolist") #Hämta alla rader från tabellen
        tasks = cur.fetchall() #Hämta result som en lista av tuples

        if tasks:
            print("All tasks")
            for task in tasks:
                print(f"ID: {task[0]}, Description: {task[1]}, Date: {task[2]}, Time: {task[3]}, Status: {'Completed' if task[4] == 1 else 'Not completed'}")
        else:
            print("No tasks are found. ")

    elif choice == "3":
        task_id = int(input("Enter the task id so you can change the task status: "))
        cur.execute(f"SELECT * FROM Todolist WHERE id = {task_id}") # Hämtar raden från tabellen Todolist där id är lika med task_id
        task = cur.fetchone() #hämtar en rad

        if task:
            print("Task found. You can now update the status.")
            new_status = int(input("Enter 0 (not completed) or 1(completed): "))
            cur.execute(f"UPDATE Todolist SET status = {new_status} WHERE id = {task_id}")
            connection.commit()
            print("Status changed")
        else:
            print("Task with the given ID does not exist")

    elif choice == "4":
        task_id = int(input("Enter task id for the task that you want to delete: "))

        cur.execute(f"SELECT * FROM Todolist WHERE id = {task_id}") # Hämtar raden från tabellen Todolist där id är lika med task_id
        task = cur.fetchone() #hämtar en rad

        if task:
            cur.execute(f"DELETE FROM todolist WHERE id = {task_id}")
            connection.commit()
            print("Task data removed")
        else:
            print("Task with the given ID does not exist")

    elif choice == "5":
        print("You quit")
        break




connection.close()