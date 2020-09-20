import sys
import sqlite3
from sqlite3 import IntegrityError

command_line_arg = sys.argv

# start a db instance
connection = sqlite3.connect('todo.db')
cursor = connection.cursor()


def create_table():
    cursor.execute("CREATE TABLE if NOT EXISTS Todos\
                    (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, Todo VARCHAR(200) UNIQUE, Status VARCHAR(10))"
                   )


create_table()
print("""
Todo app 0.0.1 (tags/v0.0.1:7b3ab59, Sep 11 2020, 23:41:10) [MSC v.1916 64 bit (AMD64) win32/debian ]
Type 'help', 'license' for more information.
    """)


#display a list of available commands
def command_help():
    """
    Usage [COMMAND] -[OPTIONS]
    commands:
            ls --list       - get a list of all your todos
            ls_cmp --list_completed
                            - get a list of all your complete todos
            ls_incmp --list_incomplete
                            - get a list of all your incomplete todos
            add             - add a todo to your todos
            rm --remove     - remove a todo from your todos
            mk --mark       - mark a todo completed
            unmk --unmark   - unmark a todo incomplete
            u --update      - make a change to an existing todo
            clear           - empty your todo list
            q --quit        - [exit]
    options:
            [add] [-m]      - add many
            [ls] [-h]       - list history: optional [-H] head, [-T] tail
            [rm] [-f] - force remove [-m] - remove many
    """


commands = [
    "ls",
    "--list",
    "ls_cmp",
    "--list_completed",
    "ls_incmp",
    "--list_incomplete",
    "add",
    "rm",
    "--remove",
    "mk",
    "--mark",
    "unmk",
    "--unmark",
    "u",
    "--update",
    "clear",
    "help",
    "licence",
]

shutdown = ["q", "quit", "--quit"]
seen_todos = False  #checks if the user has seen his todos already

# track the current number of the last todo in the database
TODO_ID_TRACKER = cursor.execute("SELECT MAX(Id) from Todos")
TODO_ID_TRACKER = cursor.fetchone()[0]


# list all the todos in the database
def ls():
    global seen_todos
    global all_todos
    all_todo = cursor.execute("SELECT * FROM Todos")
    all_todos = cursor.fetchall()
    if not any(all_todos):
        print("is empty ...")
    else:
        for i in all_todos:
            id, todo, status = i
            print(id, '\t', status, '\t', todo)
    seen_todos = True


# list only the completed todos in the database
def ls_comp():
    complete_todos = cursor.execute(
        "SELECT * FROM Todos WHERE Status = 'completed'")
    complete_todos = cursor.fetchall()
    if any(complete_todos):
        for i in complete_todos:
            id, todo, status = i
            print(id, '\t', status, '\t', todo)
    else:
        print('None')


# list only the incomplete todos in the database
def ls_incomp():
    incomplete_todos = cursor.execute(
        "SELECT * FROM Todos WHERE Status = 'incomplete'")
    incomplete_todos = cursor.fetchall()
    if any(incomplete_todos):
        for i in incomplete_todos:
            id, todo, status = i
            print(id, '\t', status, '\t', todo)
    else:
        print('None')


# add a new todo to users list of todos and set it to incomplete
def add():
    i = 0
    while True:
        add_todo = input().strip().casefold()
        if add_todo in ['q', 'quit'] or not add_todo:
            return
        if len(add_todo) < 8:
            print('sorry please leave a good description of your todo')
            add()
        else:
            try:
                cursor.execute(
                    "INSERT INTO Todos (Todo, Status) VALUES (?, 'incomplete')",
                    [add_todo])
                i += 1
                print(f'added {i} todo')
            except IntegrityError:
                print("this todo already exists")
                pass


# remove a todo from users todos
def rem():
    global seen_todos
    if not seen_todos:
        ls()

    if any(all_todos):
        todo_to_delete = input(
            "please choose a todo to delete, enter NONE to skip\n").strip(
            ).casefold()
        try:
            if todo_to_delete == 'none':
                return
            elif int(todo_to_delete) > TODO_ID_TRACKER:
                print("todo does not exist\n")
                rem()
            cursor.execute("DELETE FROM Todos WHERE Id = ?",
                           [int(todo_to_delete)])
        except ValueError:
            print('enter a valid todo ID\n')
            rem()
        if not int(todo_to_delete) > TODO_ID_TRACKER[0]:
            print(f' deleted #{todo_to_delete} successfully')
    else:
        seen_todos = False
        ls()
        print("None to delete")
        return


# set an todo as completed
def mark():
    if not seen_todos:
        ls()

    if any(all_todos):
        todo_to_mark = input(
            'please choose a todo to set as COMPLETED, enter NONE to skip\n'
        ).strip()
        try:
            if todo_to_mark == 'none':
                return
            elif int(todo_to_mark) > TODO_ID_TRACKER:
                print("todo does not exist\n")
                mark()
            cursor.execute(
                "UPDATE Todos SET Status = 'completed' WHERE Id = ?",
                [int(todo_to_mark)])
            print(f'todo #{todo_to_mark} completed')
        except ValueError:
            print("enter a valid todo ID")
            mark()
    else:
        print("ADD a TODO first!")
        return


# set a todo as incompleted
def unmark():
    if not seen_todos:
        ls()

    if any(all_todos):
        todo_to_unmark = input(
            'please choose a todo to set as INCOMPLETE, enter NONE to skip\n'
        ).strip()
        try:
            if todo_to_unmark == 'none':
                return
            elif int(todo_to_unmark) > TODO_ID_TRACKER:
                print("todo does not exist\n")
                unmark()
            cursor.execute(
                "UPDATE Todos SET Status = 'incomplete' WHERE Id = ?",
                [int(todo_to_unmark)])
            print(f'todo #{todo_to_unmark} set to incomplete')
        except ValueError:
            print("enter a valid todo ID")
            unmark()
    else:
        print("ADD a TODO first!")
        return


# edit a todo update it on the database
def update():
    if not seen_todos:
        ls()

    if any(all_todos):
        todo_to_update = input(
            "please choose a todo to EDIT, enter NONE to skip\n").strip()
        try:
            if todo_to_update == 'none':
                return
            elif int(todo_to_update) > TODO_ID_TRACKER:
                print("todo does not exist\n")
                update()
            cursor.execute("SELECT Todo FROM Todos WHERE Id = ?",
                           [int(todo_to_update)])
            print(cursor.fetchone())
            todo_to_change = input('make your changes\n')
            cursor.execute("UPDATE Todos SET Todo = ? WHERE Id = ?",
                           [todo_to_change, todo_to_update])
        except ValueError:
            print("enter a valid ID")
            update()
    else:
        print("please add a TODO")
        return


# clear all the todos by droping table and recreating it
def clear_():
    if input('are you sure you want to delete all?\n') in ['yes', 'y']:
        cursor.execute("DROP TABLE Todos")
        create_table()


if len(command_line_arg) > 1:
    help(command_help)

# start a app session for a user
while True:
    command = input(">>> ").strip().casefold()
    if command in shutdown:
        connection.commit()
        connection.close()
        quit()
    if command not in commands:
        print("i dont understand")
    if command == "help":
        help(command_help)
    if command == "license":
        print("GNU public License")
    if command in ["ls", "--list"]:
        ls()
    elif command in ["ls_cmp", "--list_completed"]:
        ls_comp()
    elif command in ["ls_incmp", "--list_incomplete"]:
        ls_incomp()
    elif command == "add":
        add()
    elif command in ["rm", "--remove"]:
        rem()
    elif command in ["mk", "--mark"]:
        mark()
    elif command in ["unmk", "--unmark"]:
        unmark()
    elif command in ["u", "--update"]:
        update()
    elif command == "clear":
        clear_()

    connection.commit()
