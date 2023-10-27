import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to the SQLite database (creates a new database file if it doesn't exist)
connection = sqlite3.connect("Emp.db")

# Create a table to store employee information
with connection:
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            department TEXT NOT NULL,
            emergency_contact_name TEXT NOT NULL,
            relationship TEXT NOT NULL,
            phone_number INTEGER NOT NULL,
            Clinical_Date INT,
            Medication_Name TEXT,
            Medical_Condition TEXT,
            Doctors_Name TEXT
        )
    """)

# Global list to store employees
employees = []

# Global text variable to hold the employee information
employees_info_text = ""


def add_function():
    # Data validation for the "Name" field
    def is_valid_name(name):
        # Name can contain alphanumeric characters, spaces, and special characters
        allowed_characters = set(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()-_=+[]{}|;:,.<>?")
        return all(char in allowed_characters for char in name)

    def save_employee_info():
        name = name_entry.get()
        position = position_entry.get()
        department = department_entry.get()
        emergency_contact_name = emergency_contact_name_entry.get()
        relationship = relationship_entry.get()
        phone_number = phone_number_entry.get()

        # Data validation to check if all fields are filled
        if not all([name, position, department, emergency_contact_name, relationship, phone_number]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Data validation for the "Name" field
        if not is_valid_name(name):
            messagebox.showerror("Error",
                                 "Name can only contain alphanumeric characters, spaces, and special characters.")
            return

        # Data validation for the "Phone Number" field
        if not phone_number.isdigit():  # Check if phone_number contains only digits
            messagebox.showerror("Error", "Phone Number must be an integer.")
            return

        # Save the employee information to the database
        with connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO employees (name, position, department, emergency_contact_name, relationship, phone_number)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, position, department, emergency_contact_name, relationship, phone_number))

        # Update the label to show the new employee's information
        employees_label.config(text="")
        show_employees()

        # Display the employee information in a custom dialog box
        display_employee_info_dialog({
            "Name": name,
            "Position": position,
            "Department": department,
            "Emergency Contact Name": emergency_contact_name,
            "Relationship": relationship,
            "Phone Number": phone_number
        })

    def display_employee_info_dialog(employee_info):
        dialog = tk.Toplevel()
        dialog.title("Employee Information")
        dialog.geometry("500x400")

        employee_details_label = tk.Label(dialog, text="Employee Information", font=("Helvetica", 14, "bold"))
        employee_details_label.pack(pady=10)

        # Create labels to display employee information
        for key, value in employee_info.items():
            employee_label = tk.Label(dialog, text=f"{key}: {value}", font=("Helvetica", 12))
            employee_label.pack(anchor="w", padx=10, pady=5)

        ok_button = tk.Button(dialog, text="OK", font=("Helvetica", 12), command=dialog.destroy)
        ok_button.pack(pady=10)

    def clear_fields():
        # Clear all the input fields
        name_entry.delete(0, tk.END)
        position_entry.delete(0, tk.END)
        department_entry.delete(0, tk.END)
        emergency_contact_name_entry.delete(0, tk.END)
        relationship_entry.delete(0, tk.END)
        phone_number_entry.delete(0, tk.END)

    registration_window = tk.Toplevel()
    registration_window.title("Register Employee")

    # Create labels
    name_label = tk.Label(registration_window, text="Name:")
    position_label = tk.Label(registration_window, text="Position:")
    department_label = tk.Label(registration_window, text="Department:")
    emergency_contact_name_label = tk.Label(registration_window, text="Emergency Contact Name:")
    relationship_label = tk.Label(registration_window, text="Relationship:")
    phone_number_label = tk.Label(registration_window, text="Phone Number:")

    # Create entry widgets
    name_entry = tk.Entry(registration_window)
    position_entry = tk.Entry(registration_window)
    department_entry = tk.Entry(registration_window)
    emergency_contact_name_entry = tk.Entry(registration_window)
    relationship_entry = tk.Entry(registration_window)
    phone_number_entry = tk.Entry(registration_window)

    # Create save button
    save_button = tk.Button(registration_window, text="Save", command=save_employee_info)
    # Create clear button
    clear_button = tk.Button(registration_window, text="Clear", command=clear_fields)
    clear_button.grid(row=4, column=3, padx=5, pady=10)

    # Grid layout for widgets
    name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    position_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    department_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    emergency_contact_name_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    relationship_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    phone_number_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")

    name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    position_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    department_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    emergency_contact_name_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    relationship_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
    phone_number_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    save_button.grid(row=7, column=1, padx=10, pady=10)


def show_employees():
    global employees_info_text
    employees_info_text = ""

    # Retrieve employee information from the database
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees")
        employees_data = cursor.fetchall()

    # Format the employee information as a string
    for employee in employees_data:
        employees_info_text += "{}\t    |   \t{}   \t|      \t{}    \t|     \t  {}  \t| \t{}    \t| \t{}    \t\n".format(
            employee[1], employee[2], employee[3], employee[4], employee[5], employee[6])

    employees_label.config(text=employees_info_text)


def view_employee():
    def search_employee():
        # Retrieve employee information from the database based on the name
        employee_name = search_entry.get()

        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employees WHERE name=?", (employee_name,))
            employee_data = cursor.fetchone()

        if employee_data:
            # Create a new window to display the employee details
            employee_details_window = tk.Toplevel()
            employee_details_window.title("Employee Details")

            # Display ID separately in a Label widget
            id_label = tk.Label(employee_details_window, text="ID:")
            id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

            id_value_label = tk.Label(employee_details_window, text=employee_data[0])
            id_value_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            # Create labels to display employee information
            labels = ["Name:", "Position:", "Department:", "Emergency Contact Name:", "Relationship:", "Phone Number:"]
            for i in range(len(labels)):
                label = tk.Label(employee_details_window, text=labels[i])
                label.grid(row=i + 1, column=0, padx=10, pady=5, sticky="e")

                # Display employee details using Label widgets (instead of Entry widgets)
                value_label = tk.Label(employee_details_window, text=employee_data[i + 1])
                value_label.grid(row=i + 1, column=1, padx=10, pady=5, sticky="w")

        else:
            messagebox.showerror("Error", f"No employee with name '{employee_name}' found.")

    search_window = tk.Toplevel()
    search_window.title("View Employee")

    search_label = tk.Label(search_window, text="Enter Employee Name:")
    search_label.pack(pady=10)

    search_entry = tk.Entry(search_window)
    search_entry.pack(pady=10)

    search_button = tk.Button(search_window, text="View Employee", command=search_employee)
    search_button.pack(pady=10)


def update_employee():
    def search_employee_by_id():
        # Retrieve employee ID from the entry widget
        employee_id = id_entry.get()

        # Validate that employee ID is an integer
        if not employee_id.isdigit():
            messagebox.showerror("Error", "Employee ID must be an integer.")
            return

        # Call the update_employee_details function with the employee ID
        update_employee_details(int(employee_id))

    update_window = tk.Toplevel()
    update_window.title("Update Employee")

    id_label = tk.Label(update_window, text="Employee ID:")
    id_label.pack(pady=10)

    id_entry = tk.Entry(update_window)
    id_entry.pack(pady=10)

    search_button = tk.Button(update_window, text="Search Employee", command=search_employee_by_id)
    search_button.pack(pady=10)


def update_employee_details(employee_id):
    def save_updated_employee_info():
        # Retrieve updated information from entry widgets
        updated_name = name_entry.get()
        updated_position = position_entry.get()
        updated_department = department_entry.get()
        updated_emergency_contact_name = emergency_contact_name_entry.get()
        updated_relationship = relationship_entry.get()
        updated_phone_number = phone_number_entry.get()
        updated_clinical_date = clinical_date_entry.get()
        updated_medication_name = medication_name_entry.get()
        updated_medical_condition = medical_condition_entry.get()
        updated_doctors_name = doctors_name_entry.get()

        # Data validation to check if all fields are filled
        if not all([updated_name, updated_position, updated_department, updated_emergency_contact_name,
                    updated_relationship, updated_phone_number, updated_clinical_date, updated_medication_name,
                    updated_medical_condition, updated_doctors_name]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        def is_valid_name(name):
            # Name can contain alphanumeric characters, spaces, and special characters
            allowed_characters = set(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()-_=+[]{}|;:,.<>?")
            return all(char in allowed_characters for char in name)
        

        # Data validation for the "Name" field
        if not is_valid_name(updated_name):
            messagebox.showerror("Error", "Name can only contain alphanumeric characters, spaces, and special characters.")
            return

        # Data validation for the "Phone Number" field
        if not updated_phone_number.isdigit():  # Check if phone_number contains only digits
            messagebox.showerror("Error", "Phone Number must be an integer.")
            return

        # Update the employee information in the database
        with connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE employees 
                SET name=?, position=?, department=?, emergency_contact_name=?, relationship=?, phone_number=?,
                clinical_date=?, medication_name=?, medical_condition=?, doctors_name=?
                WHERE id=?
            """, (updated_name, updated_position, updated_department, updated_emergency_contact_name,
                  updated_relationship, updated_phone_number, updated_clinical_date, updated_medication_name,
                  updated_medical_condition, updated_doctors_name, employee_id))

        # Show success message
        messagebox.showinfo("Success", "Employee details have been updated.")

        # Close the update window
        update_window.destroy()

        # Update the label to show the updated employee's information
        employees_label.config(text="")
        show_employees()

    def clear_fields():
        # Clear all the input fields
        name_entry.delete(0, tk.END)
        position_entry.delete(0, tk.END)
        department_entry.delete(0, tk.END)
        emergency_contact_name_entry.delete(0, tk.END)
        relationship_entry.delete(0, tk.END)
        phone_number_entry.delete(0, tk.END)
        clinical_date_entry.delete(0, tk.END)
        medication_name_entry.delete(0, tk.END)
        medical_condition_entry.delete(0, tk.END)
        doctors_name_entry.delete(0, tk.END)

    # Search for the employee details by ID
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
        employee_data = cursor.fetchone()

    if employee_data:
        # Create a new window to update the employee details
        update_window = tk.Toplevel()
        update_window.title("Update Employee Details")

        # Create labels
        name_label = tk.Label(update_window, text="Name:")
        position_label = tk.Label(update_window, text="Position:")
        department_label = tk.Label(update_window, text="Department:")
        emergency_contact_name_label = tk.Label(update_window, text="Emergency Contact Name:")
        relationship_label = tk.Label(update_window, text="Relationship:")
        phone_number_label = tk.Label(update_window, text="Phone Number:")

        # Create entry widgets
        name_entry = tk.Entry(update_window)
        position_entry = tk.Entry(update_window)
        department_entry = tk.Entry(update_window)
        emergency_contact_name_entry = tk.Entry(update_window)
        relationship_entry = tk.Entry(update_window)
        phone_number_entry = tk.Entry(update_window)

        # Create save button
        save_button = tk.Button(update_window, text="Save", command=save_updated_employee_info)
        # Create clear button
        clear_button = tk.Button(update_window, text="Clear", command=clear_fields)

        # Grid layout for widgets
        name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        position_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        department_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        emergency_contact_name_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        relationship_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        phone_number_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")

        name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        position_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        department_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        emergency_contact_name_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        relationship_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        phone_number_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Create entry widgets for the additional fields
        clinical_date_label = tk.Label(update_window, text="Clinical Date:")
        clinical_date_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
        clinical_date_entry = tk.Entry(update_window)
        clinical_date_entry.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        medication_name_label = tk.Label(update_window, text="Medication Name:")
        medication_name_label.grid(row=9, column=0, padx=10, pady=5, sticky="e")
        medication_name_entry = tk.Entry(update_window)
        medication_name_entry.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        medical_condition_label = tk.Label(update_window, text="Medical Condition:")
        medical_condition_label.grid(row=10, column=0, padx=10, pady=5, sticky="e")
        medical_condition_entry = tk.Entry(update_window)
        medical_condition_entry.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        doctors_name_label = tk.Label(update_window, text="Doctor's Name:")
        doctors_name_label.grid(row=11, column=0, padx=10, pady=5, sticky="e")
        doctors_name_entry = tk.Entry(update_window)
        doctors_name_entry.grid(row=11, column=1, padx=10, pady=5, sticky="w")

        save_button.grid(row=12, column=1, padx=10, pady=10)
        clear_button.grid(row=12, column=2, padx=10, pady=10)

        # Pre-fill entry widgets with existing employee details
        name_entry.insert(0, employee_data[1])
        position_entry.insert(0, employee_data[2])
        department_entry.insert(0, employee_data[3])
        emergency_contact_name_entry.insert(0, employee_data[4])
        relationship_entry.insert(0, employee_data[5])
        phone_number_entry.insert(0, employee_data[6])
    else:
        messagebox.showerror("Error", f"No employee with ID '{employee_id}' found.")

def delete_employee():
    def delete_employee_by_id():
        # Retrieve employee ID from the entry widget
        employee_id = id_entry.get()

        # Validate that employee ID is an integer
        if not employee_id.isdigit():
            messagebox.showerror("Error", "Employee ID must be an integer.")
            return

        # Check if the employee with the given ID exists
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
            employee_data = cursor.fetchone()

        if employee_data:
            # Confirm the deletion with a message box
            response = messagebox.askyesno("Confirm Deletion",
                                           f"Do you want to delete employee with ID {employee_id}?")
            if response == tk.YES:
                # Delete the employee from the database
                with connection:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))

                # Show success message
                messagebox.showinfo("Success", f"Employee with ID {employee_id} has been deleted.")
                # Close the delete window
                delete_window.destroy()

                # Update the label to show the updated employee list
                employees_label.config(text="")
                show_employees()

        else:
            messagebox.showerror("Error", f"No employee with ID '{employee_id}' found.")

    delete_window = tk.Toplevel()
    delete_window.title("Delete Employee")

    id_label = tk.Label(delete_window, text="Employee ID:")
    id_label.pack(pady=10)

    id_entry = tk.Entry(delete_window)
    id_entry.pack(pady=10)

    search_button = tk.Button(delete_window, text="Delete Employee", command=delete_employee_by_id)
    search_button.pack(pady=10)


def open_main_window():
    main_window = tk.Tk()
    main_window.title("Employee Management System")
    main_window.geometry("1300x280")

    welcome_label = tk.Label(main_window, text="Welcome \n Health Card System", font=("Helvetica", 20))
    welcome_label.pack(pady=10)

    # Display the column headings
    headings_text = "Name\t|\tPosition\t|\tDepartment\t|\tEmergency Contact Name\t|\tRelationship\t|\tPhone Number"
    headings_label = tk.Label(main_window, text=headings_text, font=("Helvetica", 12), justify="left", bg="#f0f0f0",
                              padx=10, pady=5)
    headings_label.pack(padx=10, pady=5)

    global employees_info_text  # Make the string variable global

    # Create a label to display employee information
    global employees_label
    employees_label = tk.Label(main_window, text=employees_info_text, font=("Helvetica", 12), justify="left",
                               bg="#f0f0f0", padx=10, pady=5)
    employees_label.pack(padx=10, pady=5)

    # Create a frame to hold the buttons
    button_frame = tk.Frame(main_window)
    button_frame.pack(pady=10)

    # Add button to open the employee registration window
    add_button = tk.Button(button_frame, text="Add Employee", font=("Helvetica", 14), command=add_function)
    add_button.pack(side=tk.LEFT, padx=10)

    # Add button to view employee details
    view_employee_button = tk.Button(button_frame, text="View Employee", font=("Helvetica", 14), command=view_employee)
    view_employee_button.pack(side=tk.LEFT, padx=10)

    # Add button to update employee details
    update_employee_button = tk.Button(button_frame, text="Update Employee", font=("Helvetica", 14),
                                       command=update_employee)
    update_employee_button.pack(side=tk.LEFT, padx=10)

    # Add button to delete employee
    delete_employee_button = tk.Button(button_frame, text="Delete Employee", font=("Helvetica", 14),
                                       command=delete_employee)
    delete_employee_button.pack(side=tk.LEFT, padx=10)

    # Show the existing employees' information
    show_employees()

    main_window.mainloop()


# Open the main window
open_main_window()
