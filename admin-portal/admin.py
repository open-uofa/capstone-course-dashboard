"""Command line admin console for capstone dashboard app"""
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from tabulate import tabulate

path = "../backend/app/server/.env"
load_dotenv(dotenv_path=path, verbose=True)
client = MongoClient(os.getenv("MONGODB_ADDRESS"))
db = client[os.getenv("DB_NAME")]

""" Login to the admin page. After 5 failed attempts, the program will exit. """


def login_admin():
    """Verify the username and password for the admin page."""
    
    count = 0
    correct_credentials = False
    while correct_credentials is False:

        user_name = input("Enter username: ")
        password = input("Enter password: ")
        coll = db["admin"].find_one({"username": user_name, "password": password})

        if coll is None:
            print("Wrong username or password")
        else:
            correct_credentials = True
            print("Login successful")

        count += 1

        if count == 5:
            print("5 failed attempts, exiting")
            return False
    return True


def get_user_list():
    """Get the list of users from the database."""
    coll = db["user"].find()
    user_list = []
    i = 1
    for user in coll:
        if "assigned_courses" not in user.keys():
            user_list.append([i, user["email"], "None", user["authorized"]])
        else:
            user_list.append(
                [i, user["email"], str(user["assigned_courses"]), str(user["authorized"])]
            )
        i += 1

    print(
        tabulate(user_list, headers=["Pos", "Email", "Assigned Courses", "Authorized"])
    )


def add_user():
    """Add a user to the database."""
    email = input("Enter email: ")
    assigned_courses = input("Enter assigned course names separted by ',' : ").split(",")
    authorized = input("Enter authorized (Y/N): ")

    authorized = authorized.lower() == "y" or authorized.lower() == "yes"

    if len(assigned_courses) == 1 and assigned_courses[0] != "":
        result = db["user"].insert_one(
            {
                "email": email,
                "assigned_courses": [assigned_courses[0]],
                "authorized": authorized,
            }
        )

        if result.inserted_id:
            print("Success! User added")
    elif len(assigned_courses) == 1 and assigned_courses[0] == "":
        result = db["user"].insert_one(
            {
                "email": email,
                "authorized": authorized,
            }
        )

        if result.inserted_id:
            print("Success! User added")
    else:
        result = db["user"].insert_one(
            {
                "email": email,
                "assigned_courses": [assigned_courses[0]],
                "authorized": authorized,
            }
        )
        if result.inserted_id:
            print("Success! User added")
        for x in range(1, len(assigned_courses)):
            result = db["user"].update_one(
                {"email": email}, {"$push": {"assigned_courses": assigned_courses[x]}}
            )
        

def delete_user():
    """Delete a user from the database."""
    email = input("Enter email of the user you want to delete: ")
    result = db["user"].delete_one({"email": email})

    if result.deleted_count == 0:
        print("User not found")

    else:
        print("Success! User deleted")


def revoke_user():
    """Revoke a user's authorization."""
    email = input("Enter email of the user you want to revoke : ")
    result = db["user"].update_one({"email": email}, {"$set": {"authorized": False}})

    if result.modified_count == 0:
        print("User not found")
    else:
        print("Success! User access revoked")


def assign_courses():
    """Assign courses to a user."""
    email = input("Enter email of the user you want to assign courses to: ")
    assigned_courses = input("Enter course names separated by ',' : ").split(",")
    
    for x in range(0, len(assigned_courses)):
        result = db["user"].update_one(
            {"email": email}, {"$push": {"assigned_courses": assigned_courses[x]}}
        )
    
        if result.modified_count == 0:
            print("Operation failed. Could not assign " + assigned_courses[x])
        else:
            print("Success! " + assigned_courses[x] + " assigned")


def unassign_courses():
    """Unassign courses from a user."""
    email = input("Enter email of the user you want to unassign courses from: ")
    assigned_courses = input("Enter course names separated by ',': ").split(",")

    for x in range(0, len(assigned_courses)):
        result = db["user"].update_one(
            {"email": email}, {"$pull": {"assigned_courses": assigned_courses[x]}}
        )

        if result.modified_count == 0:
            print("Operation failed. Could not unassign " + assigned_courses[x])
        else:
            print("Success! " + assigned_courses[x] + " unassigned")
    

def authorize_user():
    """Authorize a user."""
    email = input("Enter email of the user you want to authorize: ")
    result = db["user"].update_one({"email": email}, {"$set": {"authorized": True}})

    if result.modified_count == 0:
        print("User not found")
    else:
        print("Success! User authorized")


if __name__ == "__main__":

    if login_admin():
        while True:
            print("1. Get user list")
            print("2. Add user")
            print("3. Delete user")
            print("4. Revoke user")
            print("5. Assign courses")
            print("6. Unassign courses")
            print("7. Authorize user")
            print("8. Exit")
            choice = input("Enter choice: ")
            if choice == "1":
                get_user_list()
            elif choice == "2":
                add_user()
            elif choice == "3":
                delete_user()
            elif choice == "4":
                revoke_user()
            elif choice == "5":
                assign_courses()
            elif choice == "6":
                unassign_courses()
            elif choice == "7":
                authorize_user()
            elif choice == "8":
                break
            else:
                print("Invalid choice")
