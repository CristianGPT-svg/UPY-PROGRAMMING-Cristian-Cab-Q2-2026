# ============================================================
# Classwork #10 - School Management System
# ============================================================

# ---- DATA ----

# INPUT - Fixed tuple of subjects (never changes during execution)
subjects = (
    "Discrete Mathematics",
    "Programming",
    "English II",
    "Differential Calculus",
    "Probability and Statistics",
    "Computer and Server Architecture",
    "Socio-Emotional Skills and Conflict Management"
)

# INPUT - Users dictionary with password, role, and name
users = {
    'jperez':   {'password': '1234', 'rol': 'student',     'name': 'Juan Perez'},
    'dromo':    {'password': '1234', 'rol': 'student',     'name': 'Daniela Romo'},
    'mjuarez':  {'password': '1234', 'rol': 'student',     'name': 'Mauricio Juarez'},
    'mlopez':   {'password': '1234', 'rol': 'student',     'name': 'Maria Lopez'},
    'euc':      {'password': '1234', 'rol': 'student',     'name': 'Ernesto Uc'},
    'cbalam':   {'password': '1234', 'rol': 'student',     'name': 'Carlos Balam'},
    'jpedrozo': {'password': '1234', 'rol': 'professor',   'name': 'Jorge Pedrozo'},
    'dgamboa':  {'password': '1234', 'rol': 'coordinator', 'name': 'Didier Gamboa'},
}

# INPUT - Grades dictionary; keys match student usernames in users
notes = {
    'jperez': {
        'Discrete Mathematics': 8.5,
        'Programming': 9.2,
        'English II': 9.0,
        'Differential Calculus': 7.8,
        'Probability and Statistics': 8.3,
        'Computer and Server Architecture': 6.8,
        'Socio-Emotional Skills and Conflict Management': 9.5
    },
    'dromo': {
        'Discrete Mathematics': 9.0,
        'Programming': 6.7,
        'English II': 9.4,
        'Differential Calculus': 6.2,
        'Probability and Statistics': 9.1,
        'Computer and Server Architecture': 6.5,
        'Socio-Emotional Skills and Conflict Management': 9.8
    },
    'mjuarez': {
        'Discrete Mathematics': 7.5,
        'Programming': 8.0,
        'English II': 8.5,
        'Differential Calculus': 7.0,
        'Probability and Statistics': 7.8,
        'Computer and Server Architecture': 6.2,
        'Socio-Emotional Skills and Conflict Management': 8.9
    },
    'mlopez': {
        'Discrete Mathematics': 9.5,
        'Programming': 9.8,
        'English II': 9.2,
        'Differential Calculus': 9.0,
        'Probability and Statistics': 9.6,
        'Computer and Server Architecture': 9.4,
        'Socio-Emotional Skills and Conflict Management': 10.0
    },
    'euc': {
        'Discrete Mathematics': 8.2,
        'Programming': 6.9,
        'English II': 8.8,
        'Differential Calculus': 6.0,
        'Probability and Statistics': 6.4,
        'Computer and Server Architecture': 8.1,
        'Socio-Emotional Skills and Conflict Management': 9.0
    },
    'cbalam': {
        'Discrete Mathematics': 8.8,
        'Programming': 9.0,
        'English II': 8.5,
        'Differential Calculus': 6.6,
        'Probability and Statistics': 8.9,
        'Computer and Server Architecture': 8.7,
        'Socio-Emotional Skills and Conflict Management': 9.2
    },
}

# ============================================================
# LOGIN LOOP
# ============================================================

print("=" * 45)
print("       School Management System")
print("=" * 45)

# PROCESS - Keep asking until credentials match (unlimited attempts)
while True:
    # INPUT - Ask for username and password
    username = input("\nUsername: ").strip()
    password = input("Password: ").strip()

    # PROCESS - Validate against users dictionary
    if username in users and users[username]['password'] == password:
        name = users[username]['name']
        rol  = users[username]['rol']

        # OUTPUT - Welcome message
        print("\nWelcome, " + name + " (" + rol + ")")

        # ============================================================
        # STUDENT MENU
        # ============================================================
        if rol == 'student':

            # PROCESS - Retrieve grades
            grades = notes[username]

            # PROCESS - Build sets: passed (>= 7.0) and pending (set difference)
            passed  = {s for s in subjects if grades[s] >= 7.0}
            pending = set(subjects) - passed

            # OUTPUT - Print only passed subjects as a table
            print("\n--- Report Card: " + name + " ---")

            col_w = 46
            sep = "  +" + "-" * (col_w + 2) + "+" + "-" * 8 + "+"
            print(sep)
            print("  | {:<{w}} | {:>5}  |".format("Subject", "Grade", w=col_w))
            print(sep)
            for subject in subjects:
                if subject in passed:
                    print("  | {:<{w}} | {:>5.1f}  |".format(subject, grades[subject], w=col_w))
            print(sep)

            # OUTPUT - Total passed count and list
            print("\nPassed subjects (" + str(len(passed)) + " of " + str(len(subjects)) + "):")
            for s in subjects:
                if s in passed:
                    print("  [+] " + s)

            # OUTPUT - Pending subjects
            if pending:
                print("\nPending subjects (" + str(len(pending)) + "):")
                for s in subjects:
                    if s in pending:
                        print("  [-] " + s)
            else:
                print("\nAll subjects passed!")

        # ============================================================
        # PROFESSOR MENU
        # ============================================================
        elif rol == 'professor':

            # OUTPUT - List all students
            print("\n--- Registered Students ---")
            for user, data in users.items():           # PROCESS - Filter by role
                if data['rol'] == 'student':
                    print("  " + user + " - " + data['name'])

            # PROCESS - Loop: professor can update multiple grades until 'exit'
            while True:
                # INPUT - Ask which student (or exit)
                student = input("\nEnter student username (or 'exit' to quit): ").strip()
                if student.lower() == 'exit':
                    print("Exiting professor menu.")
                    break
                if student not in notes:
                    print("Username not found or not a student. Try again.")
                    continue

                # OUTPUT - Show student's current grades as a table
                print("\nCurrent grades for " + users[student]['name'] + ":")
                col_w = 46
                sep = "  +" + "-" * (col_w + 2) + "+" + "-" * 8 + "+"
                print(sep)
                print("  | {:<{w}} | {:>5}  |".format("Subject", "Grade", w=col_w))
                print(sep)
                for subject in subjects:
                    print("  | {:<{w}} | {:>5.1f}  |".format(subject, notes[student][subject], w=col_w))
                print(sep)

                # INPUT - Ask which subject
                subject = input("Subject to edit: ").strip()
                if subject not in subjects:
                    print("Invalid subject. Try again.")
                    continue

                # INPUT - Ask for new grade
                try:
                    new_grade = float(input("New grade: "))
                except ValueError:
                    print("Invalid grade. Try again.")
                    continue

                # INPUT - Confirm before saving
                current = notes[student][subject]
                print("Change " + subject + " for " + users[student]['name'] +
                      " from " + str(current) + " to " + str(new_grade) + "?")
                confirm = input("Are you sure? (yes / no): ").strip().lower()

                if confirm == 'yes':
                    # PROCESS - Overwrite grade in notes dictionary
                    notes[student][subject] = new_grade
                    # OUTPUT - Confirm the change
                    print("Grade updated successfully.")
                else:
                    # OUTPUT - Cancelled
                    print("Change cancelled. Grade not modified.")

        # ============================================================
        # COORDINATOR MENU
        # ============================================================
        elif rol == 'coordinator':

            # OUTPUT - List professors
            print("\n--- Professors ---")
            for user, data in users.items():           # PROCESS - Filter by role
                if data['rol'] == 'professor':
                    print("  " + user + " - " + data['name'])

            # OUTPUT - List subjects from tuple
            print("\n--- Subjects ---")
            for subject in subjects:
                print("  " + subject)

            # OUTPUT - One combined table: students as rows, subjects as columns
            print("\n--- Students & Grades ---")

            # PROCESS - Column widths
            name_w   = 20
            grade_w  = 8
            short_hdrs = [s[:grade_w] for s in subjects]

            sep = "+" + "-" * (name_w + 2) + ("+" + "-" * (grade_w + 2)) * len(subjects) + "+"
            print(sep)

            header = "| {:<{nw}} ".format("Student", nw=name_w)
            for h in short_hdrs:
                header += "| {:<{gw}} ".format(h, gw=grade_w)
            header += "|"
            print(header)
            print(sep)

            # PROCESS - One row per student
            for student, grades in notes.items():
                student_name = users[student]['name']
                row = "| {:<{nw}} ".format(student_name[:name_w], nw=name_w)
                for subject in subjects:
                    row += "| {:>{gw}.1f} ".format(grades[subject], gw=grade_w)
                row += "|"
                print(row)

            print(sep)

        break   # Exit login loop after successful session

    else:
        # OUTPUT - Invalid credentials, loop again
        print("Invalid username or password. Please try again.")
