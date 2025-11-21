import json
import os
import sys
from typing import List, Dict, Any, Optional

USERS_FILE = "users.json"
STUDENTS_FILE = "students.json"


# ---------------------- JSON File Helpers ---------------------- #

def load_json(filename: str, default):
    """Load JSON data from file, or return default if not found/invalid."""
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(filename: str, data):
    """Save JSON data to file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_users() -> List[Dict[str, Any]]:
    return load_json(USERS_FILE, [])


def save_users(users: List[Dict[str, Any]]):
    save_json(USERS_FILE, users)


def load_students() -> List[Dict[str, Any]]:
    return load_json(STUDENTS_FILE, [])


def save_students(students: List[Dict[str, Any]]):
    save_json(STUDENTS_FILE, students)


def get_next_student_id(students: List[Dict[str, Any]]) -> int:
    if not students:
        return 1
    return max(s["id"] for s in students) + 1


# ---------------------- User Authentication ---------------------- #

def signup():
    """Register a new user (simple username + password)."""
    print("\n===== Signup =====")
    users = load_users()
    username = input("Enter a new username: ").strip()

    # Check if username already exists
    if any(u["username"] == username for u in users):
        print("Username already exists. Please choose another or login.\n")
        return

    password = input("Enter a password: ").strip()
    if not password:
        print("Password cannot be empty.\n")
        return

    users.append({
        "username": username,
        "password": password
    })
    save_users(users)
    print("Signup successful! You can now login.\n")


def login() -> Optional[str]:
    """Login existing user. Returns username if success, else None."""
    print("\n===== Login =====")
    users = load_users()
    if not users:
        print("No users registered yet. Please signup first.\n")
        return None

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    for u in users:
        if u["username"] == username and u["password"] == password:
            print(f"\nWelcome, {username}!\n")
            return username

    print("Invalid username or password.\n")
    return None


# ---------------------- Student Operations ---------------------- #

def add_student():
    print("\n===== Add New Student =====")
    name = input("Student Name: ").strip()
    roll_no = input("Roll Number: ").strip()
    class_name = input("Class: ").strip()
    section = input("Section: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()

    if not name or not roll_no or not class_name:
        print("Name, Roll Number and Class are required fields.\n")
        return

    students = load_students()

    # Check for unique roll number
    if any(s["roll_no"] == roll_no for s in students):
        print("A student with this roll number already exists.\n")
        return

    new_student = {
        "id": get_next_student_id(students),
        "name": name,
        "roll_no": roll_no,
        "class_name": class_name,
        "section": section,
        "email": email,
        "phone": phone
    }

    students.append(new_student)
    save_students(students)
    print("Student added successfully.\n")


def print_student(student: Dict[str, Any]):
    print(f"ID: {student['id']}")
    print(f"Name: {student['name']}")
    print(f"Roll No: {student['roll_no']}")
    print(f"Class: {student['class_name']}  Section: {student['section']}")
    print(f"Email: {student['email']}")
    print(f"Phone: {student['phone']}")
    print("-" * 40)


def view_all_students():
    print("\n===== All Students =====")
    students = load_students()
    if not students:
        print("No student records found.\n")
        return
    # Sort by ID
    students_sorted = sorted(students, key=lambda s: s["id"])
    for s in students_sorted:
        print_student(s)


def search_student_by_roll():
    print("\n===== Search Student by Roll Number =====")
    roll_no = input("Enter Roll Number: ").strip()
    students = load_students()
    for s in students:
        if s["roll_no"] == roll_no:
            print("\nStudent found:\n")
            print_student(s)
            return
    print("No student found with this roll number.\n")


def update_student():
    print("\n===== Update Student =====")
    roll_no = input("Enter Roll Number of student to update: ").strip()
    students = load_students()

    for s in students:
        if s["roll_no"] == roll_no:
            print("\nCurrent details (leave blank to keep existing value):")
            new_name = input(f"Name [{s['name']}]: ").strip() or s["name"]
            new_class = input(f"Class [{s['class_name']}]: ").strip() or s["class_name"]
            new_section = input(f"Section [{s['section']}]: ").strip() or s["section"]
            new_email = input(f"Email [{s['email']}]: ").strip() or s["email"]
            new_phone = input(f"Phone [{s['phone']}]: ").strip() or s["phone"]

            s["name"] = new_name
            s["class_name"] = new_class
            s["section"] = new_section
            s["email"] = new_email
            s["phone"] = new_phone

            save_students(students)
            print("Student updated successfully.\n")
            return

    print("No student found with this roll number.\n")


def delete_student():
    print("\n===== Delete Student =====")
    roll_no = input("Enter Roll Number of student to delete: ").strip()
    students = load_students()

    for s in students:
        if s["roll_no"] == roll_no:
            confirm = input(
                f"Are you sure you want to delete {s['name']} (Roll: {roll_no})? (y/n): "
            ).strip().lower()
            if confirm == "y":
                students = [st for st in students if st["roll_no"] != roll_no]
                save_students(students)
                print("Student deleted successfully.\n")
            else:
                print("Delete cancelled.\n")
            return

    print("No student found with this roll number.\n")


# ---------------------- Logged-in Menu ---------------------- #

def student_management_menu(username: str):
    """Menu shown after successful login. Includes logout feature."""
    while True:
        print("=====================================")
        print(f"   STUDENT MANAGEMENT DASHBOARD")
        print(f"   Logged in as: {username}")
        print("=====================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by Roll Number")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Logout")
        print("0. Exit Application")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student_by_roll()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("\nLogging out...\n")
            break   # go back to main menu
        elif choice == "0":
            print("\nExiting application. Goodbye!\n")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.\n")


# ---------------------- Main Menu ---------------------- #

def main():
    print("=====================================")
    print("        STUDENT MANAGEMENT SYSTEM    ")
    print("=====================================")

    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            user = login()
            if user:
                student_management_menu(user)   # after login
        elif choice == "2":
            signup()
        elif choice == "3":
            print("\nThank you for using Student Management System.\n")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
