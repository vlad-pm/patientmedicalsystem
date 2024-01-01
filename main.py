import PySimpleGUI as sg
import mysql.connector
from datetime import datetime
from tblInfo import * 
from database import dbHost, dbUser, dbPassword

global version
version = 'V0.0.5'

#sql db connection
mysqldb = mysql.connector.connect(
    host = f"{dbHost}",
    user = f"{dbUser}",
    password = f"{dbPassword}"
    )
db = mysqldb.cursor(buffered=True)

db.execute("CREATE DATABASE IF NOT EXISTS patientmedicalsystem")
db.execute("USE patientmedicalsystem;")

db.execute(f"CREATE TABLE IF NOT EXISTS accounts ({tblAccountsColumns})")
db.execute(f"CREATE TABLE IF NOT EXISTS patients ({tblPatientColumns})")
db.execute(f"CREATE TABLE IF NOT EXISTS doctors ({tblDoctorColumns})")
db.execute(f"CREATE TABLE IF NOT EXISTS appointments ({tblAppointmentsColumns})")
mysqldb.commit()

sg.theme('BlueMono')   # Medical colour seems fitting.

def loginMethod():
    global allowEntry
    allowEntry = False
    loginLayout = [
        [sg.Text('Welcome to the Patient Management System (PMS). ' +version, font=16)],
        [sg.Text('Username', size =(15, 1), font=14), sg.InputText(key='-username-', font=14)],
        [sg.Text('Password', size =(15, 1), font=14), sg.InputText(key = '-password-', font=14, password_char='*')],
        [sg.Button('Login'), sg.Button('Create Account'), sg.Button('Cancel')]
        ]
    # Create the log in window
    loginWindow = sg.Window('PMS Log In '+version, loginLayout)
    successfulLogin = True 
    def createAccount(usernamein, passwordin):
        sql = "INSERT INTO accounts(username, password) VALUES (%s, %s)"
        vals = usernamein, passwordin
        db.execute(sql,vals)
        mysqldb.commit()
        print("An account has been created for user " + usernamein + " at " + str(datetime.now()))
        sg.popup_ok("You have successfully created an account. Please log in to access the system!")

    def login(usernamein,passwordin):
        global successfulLogin
        successfulLogin = False
        getUserDetails = ("SELECT count(*) FROM accounts WHERE username = %(user)s and password = %(pass)s GROUP BY username,password")
        db.execute(getUserDetails, { 'user' : usernamein, 'pass' : passwordin } )
        checkAccount = db.fetchone()
        if checkAccount[0] == 1:
            print("User " + usernamein + " has successfully logged in at " + str(datetime.now()))
            sg.popup_ok("Successfully logged as " + usernamein)
            loginWindow.close()
            homeScreenMethod()
        elif checkAccount[0] == 0:
            print("User " + usernamein + " has attempted a log in but an account could not be found")
            sg.popup_ok("An account under " + usernamein + " could not be found. Please try again or create a new account.")
        else:
            print("An unhandled error has occured")


    while True:
        event, values = loginWindow.read()
        if event == 'Create Account':
            if not values['-username-'] or not values['-password-']:
                sg.popup_ok("You must enter a username and password.")
            else:
                createAccount(values['-username-'], values['-password-'])
            
        if event == 'Login':
            login(values['-username-'], values['-password-'])
        
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
    
    if successfulLogin == True:
        allowEntry = True


def homeScreenMethod():
    
    
    menu_def = [
        ['Home', []],
        ['Patients', ['Add Patient', 'View Patients']],
        ['Appointments', ['Make Appointment', 'View Appointments']],
        ['Doctors', ['Add Doctor', 'View Doctors']],
    ]
    
    homeLayout = [
        [sg.Menu(menu_def)],
        [sg.Multiline("", key='-IN-',expand_x=True, expand_y=True)],
        [sg.Multiline("", key='-OUT-',expand_x=True, expand_y=True)],
        [sg.Multiline("", key='-TXT-',expand_x=True, expand_y=True,font=("Arial Bold", 14))]
    ] 

    menu_bar = sg.Menu(menu_def, tearoff=True)

    # Create the home screen window
    homeScreenWindow = sg.Window('PMS Home '+version, homeLayout)
    while True:
            event, values = homeScreenWindow.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "Add Patient":
                showAddPatient()
            elif event == "Make Appointment":
                showBookAppointment()
            elif event == "Add Doctor":
                showAddDoctor()
            elif event == "View Patients":
                showViewPatients()
            elif event == "View Appointments":
                showViewAppointments()
            elif event == "View Doctors":
                showViewDoctors()

def showAddPatient():
    global salutationList
    salutationList = ['Mr', 'Miss', 'Ms', 'Mrs', 'Mx']
    addPatientLayout = [  [sg.Text('Please enter the required details for a new patient ' +version, font=16)],
                [sg.Text('Salutation', size =(15, 1), font=14), sg.Combo(salutationList, key='-newPatientSalutation-', font=14)],
                [sg.Text('First Name', size =(15, 1), font=14), sg.InputText(key = '-newPatientFirstName-', font=14)],
                [sg.Text('Surname', size =(15, 1), font=14), sg.InputText(key = '-newPatientSurname-', font=14)],
                [sg.Text('Email', size =(15, 1), font=14), sg.InputText(key = '-newPatientEmail-', font=14)],
                [sg.Text('Phone Number', size =(15, 1), font=14), sg.InputText(key = '-newPatientPhoneNo-', font=14)],
                [sg.Text('Address line 1', size =(15, 1), font=14), sg.InputText(key = '-newPatientAL1-', font=14)],
                [sg.Text('Address line 2', size =(15, 1), font=14), sg.InputText(key = '-newPatientAL2-', font=14)],
                [sg.Text('Town', size =(15, 1), font=14), sg.InputText(key = '-newPatientTown-', font=14)],
                [sg.Text('Postcode', size =(15, 1), font=14), sg.InputText(key = '-newPatientPostcode-', font=14)],
                [sg.Button('Add Patient'), sg.Button('Cancel')]
                    ]
    
    newPatientWindow = sg.Window('PMS Add Patient '+version, addPatientLayout)
    
    def createPatient(salutationin, firstnamein, surnamein, emailin, phonenumberin, addressline1in, addressline2in, townin, postcodein):
        # check for nulls before inserting - avoids poor quality data
        if not salutationin or not firstnamein or not surnamein:
            sg.popup_ok("Please fill in all required fields.")
            return  # exit if any required is null
        else:
            sql = "INSERT INTO patients(salutation, first_name, surname, email, phone_number, first_line_address, second_line_address, town, postcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )"
            vals = salutationin, firstnamein, surnamein, emailin, phonenumberin, addressline1in, addressline2in, townin, postcodein
            db.execute(sql,vals)
            mysqldb.commit()
            print(salutationin + " " + firstnamein + " " + surnamein + " has been added as a patient at " + str(datetime.now()))
            sg.popup_ok("You have successfully added " + salutationin + " " + firstnamein + " " + surnamein + " as a patient.")
            newPatientWindow.close()
            


    while True:
            event, values = newPatientWindow.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                newPatientWindow.close()
                break
            if event == "Add Patient":
                createPatient(values['-newPatientSalutation-'], values['-newPatientFirstName-'], values['-newPatientSurname-'], values['-newPatientEmail-'], values['-newPatientPhoneNo-'], values['-newPatientAL1-'], values['-newPatientAL2-'], values['-newPatientTown-'], values['-newPatientPostcode-'])

def showViewPatients():
    selected_patient_id = None 
    db.execute("SELECT * FROM patients")
    patients_data = db.fetchall()
    patient_layout = []
    headings = ['ID', 'Salutation', 'First Name', 'Surname', 'Email', 'Phone Number', 'Address Line 1', 'Address Line 2', 'Town', 'Postcode']
    data = [[str(patient[0]), patient[1], patient[2], patient[4], patient[5], patient[6], patient[7], patient[8], patient[9]] for patient in patients_data]
    view_patients_layout = [
        [sg.Table(values=data, headings=headings, auto_size_columns=True, justification='right',
                  num_rows=min(25, len(data)), enable_events=True, key='-TABLE-',
                  col_widths=[5, 10, 15, 15, 20, 15, 20, 20, 15, 15],
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.Button('Change Details'), sg.Button('Delete Patient'), sg.Button('Close')]
    ]

    view_patients_window = sg.Window('View Patients ' + version, view_patients_layout)


    while True:
        event, values = view_patients_window.read()

        if event == sg.WIN_CLOSED or event == 'Close':
            view_patients_window.close()
            break


        # check if patient is selected
        if '-TABLE-' in event:
            row_index = values['-TABLE-'][0]
            # update selected array with selected record
            selected_patient_id = data[row_index][0]


        if event == 'Change Details' and selected_patient_id:
            # retrieve the selected patient's details
            db.execute("SELECT * FROM patients WHERE id = %s", (selected_patient_id,))
            selected_patient_data = db.fetchone()

            change_details_layout = [
                [sg.Text('Change Details', font=16)],
                [sg.Text('First Name', size=(15, 1), font=14), sg.InputText(key='-changeFirstName-', default_text=selected_patient_data[1], font=14)],
                [sg.Text('Surname', size=(15, 1), font=14), sg.InputText(key='-changeSurname-', default_text=selected_patient_data[2], font=14)],
                [sg.Text('Email', size=(15, 1), font=14), sg.InputText(key='-changeEmail-', default_text=selected_patient_data[4], font=14)],
                [sg.Text('Phone Number', size=(15, 1), font=14), sg.InputText(key='-changePhoneNo-', default_text=selected_patient_data[5], font=14)],
                [sg.Text('Address line 1', size=(15, 1), font=14), sg.InputText(key='-changeAL1-', default_text=selected_patient_data[6], font=14)],
                [sg.Text('Address line 2', size=(15, 1), font=14), sg.InputText(key='-changeAL2-', default_text=selected_patient_data[7], font=14)],
                [sg.Text('Town', size=(15, 1), font=14), sg.InputText(key='-changeTown-', default_text=selected_patient_data[8], font=14)],
                [sg.Text('Postcode', size=(15, 1), font=14), sg.InputText(key='-changePostcode-', default_text=selected_patient_data[9], font=14)],
                [sg.Button('Save Changes'), sg.Button('Cancel')]
            ]

            change_details_window = sg.Window('Change Patient Details ' + version, change_details_layout)

            while True:
                change_event, change_values = change_details_window.read()

                if change_event == sg.WIN_CLOSED or change_event == 'Cancel':
                    change_details_window.close()
                    break

                if change_event == 'Save Changes':
                    update_sql = """
                        UPDATE patients
                        SET first_name = %s, surname = %s, email = %s, phone_number = %s,
                            first_line_address = %s, second_line_address = %s, town = %s, postcode = %s
                        WHERE id = %s
                    """
                    update_vals = (
                        change_values['-changeFirstName-'], change_values['-changeSurname-'],
                        change_values['-changeEmail-'], change_values['-changePhoneNo-'],
                        change_values['-changeAL1-'], change_values['-changeAL2-'],
                        change_values['-changeTown-'], change_values['-changePostcode-'],
                        selected_patient_id
                    )
                    db.execute(update_sql, update_vals)
                    mysqldb.commit()
                    sg.popup_ok("Patient details updated successfully.")

                    change_details_window.close()
                    showViewPatients()
                    

        if event == 'Delete Patient' and selected_patient_id:
            confirm_delete = sg.popup_yes_no(f"Do you really want to delete patient with ID {selected_patient_id}?")
            if confirm_delete == 'Yes':
                delete_sql = "DELETE FROM patients WHERE id = %s"
                db.execute(delete_sql, (selected_patient_id,))
                mysqldb.commit()
                sg.popup_ok(f"Patient with ID {selected_patient_id} deleted.")
                change_details_window.close()
                showViewPatients()

def showAddDoctor():

    doctorLayout = [
        [sg.Text('Please enter the required details for a new doctor ' + version, font=16)],
        [sg.Text('Salutation', size=(15, 1), font=14), sg.Combo(['Mr', 'Miss', 'Ms', 'Mrs', 'Mx'], key='-doctorSalutation-', font=14)],
        [sg.Text('First Name', size=(15, 1), font=14), sg.InputText(key='-doctorFirstName-', font=14)],
        [sg.Text('Surname', size=(15, 1), font=14), sg.InputText(key='-doctorSurname-', font=14)],
        [sg.Text('Email', size=(15, 1), font=14), sg.InputText(key='-doctorEmail-', font=14)],
        [sg.Text('Department', size=(15, 1), font=14), sg.InputText(key='-doctorDepartment-', font=14)],
        [sg.Button('Add Doctor'), sg.Button('Cancel')]
    ]

    addDoctorWindow = sg.Window('PMS Add Doctor ' + version, doctorLayout)

    def addDoctor(salutation, first_name, surname, email, department):
        if not salutation or not first_name or not surname or not email or not department:
            sg.popup_ok("Please fill in all required fields.")
            return

        sql = "INSERT INTO doctors(salutation, first_name, surname, email, department) VALUES (%s, %s, %s, %s, %s)"
        vals = salutation, first_name, surname, email, department
        db.execute(sql, vals)
        mysqldb.commit()
        print("Doctor", first_name, surname, "added successfully")

    while True:
        event, values = addDoctorWindow.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            addDoctorWindow.close()
            break
        if event == "Add Doctor":
            addDoctor(values['-doctorSalutation-'], values['-doctorFirstName-'], values['-doctorSurname-'],
                     values['-doctorEmail-'], values['-doctorDepartment-'])
            addDoctorWindow.close()

def showViewDoctors():
    selected_doctor_id = None

    db.execute("SELECT * FROM doctors")
    doctors_data = db.fetchall()

    doctor_layout = []
    headings = ['ID', 'Salutation', 'First Name', 'Surname', 'Email', 'Department']
    data = [[str(doctor[0]), doctor[1], doctor[2], doctor[3], doctor[4], doctor[5]] for doctor in doctors_data]

    view_doctors_layout = [
        [sg.Table(values=data, headings=headings, auto_size_columns=True, justification='right',
                  num_rows=min(25, len(data)), enable_events=True, key='-TABLE-',
                  col_widths=[5, 10, 15, 15, 20, 20],
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.Button('Change Details'), sg.Button('Delete Doctor'), sg.Button('Close')]
    ]

    view_doctors_window = sg.Window('View Doctors ' + version, view_doctors_layout)

    while True:
        event, values = view_doctors_window.read()

        if event == sg.WIN_CLOSED or event == 'Close':
            view_doctors_window.close()
            break

        if '-TABLE-' in event:
            row_index = values['-TABLE-'][0]
            # update selected array with selected record
            selected_doctor_id = data[row_index][0]

        if event == 'Change Details' and selected_doctor_id is not None:
            db.execute("SELECT * FROM doctors WHERE id = %s", (selected_doctor_id,))
            selected_doctor_data = db.fetchone()

            change_details_layout = [
                [sg.Text('Change Details', font=16)],
                [sg.Text('Salutation', size=(15, 1), font=14), sg.InputText(key='-changeDoctorSalutation-', default_text=selected_doctor_data[1], font=14)],
                [sg.Text('First Name', size=(15, 1), font=14), sg.InputText(key='-changeDoctorFirstName-', default_text=selected_doctor_data[2], font=14)],
                [sg.Text('Surname', size=(15, 1), font=14), sg.InputText(key='-changeDoctorSurname-', default_text=selected_doctor_data[3], font=14)],
                [sg.Text('Email', size=(15, 1), font=14), sg.InputText(key='-changeDoctorEmail-', default_text=selected_doctor_data[4], font=14)],
                [sg.Text('Department', size=(15, 1), font=14), sg.InputText(key='-changeDoctorDepartment-', default_text=selected_doctor_data[5], font=14)],
                [sg.Button('Save Changes'), sg.Button('Cancel')]
            ]

            change_details_window = sg.Window('Change Doctor Details ' + version, change_details_layout)

            while True:
                change_event, change_values = change_details_window.read()

                if change_event == sg.WIN_CLOSED or change_event == 'Cancel':
                    change_details_window.close()
                    break

                if change_event == 'Save Changes':
                    update_sql = """
                        UPDATE doctors
                        SET salutation = %s, first_name = %s, surname = %s, email = %s, department = %s
                        WHERE id = %s
                    """
                    update_vals = (
                        change_values['-changeDoctorSalutation-'], change_values['-changeDoctorFirstName-'],
                        change_values['-changeDoctorSurname-'], change_values['-changeDoctorEmail-'],
                        change_values['-changeDoctorDepartment-'], selected_doctor_id
                    )
                    db.execute(update_sql, update_vals)
                    mysqldb.commit()
                    sg.popup_ok("Doctor details updated successfully.")
                    change_details_window.close()
                    showViewDoctors()
                    

        if event == 'Delete Doctor' and selected_doctor_id is not None:
            confirm_delete = sg.popup_yes_no(f"Do you really want to delete doctor with ID {selected_doctor_id}?")
            if confirm_delete == 'Yes':
                delete_sql = "DELETE FROM doctors WHERE id = %s"
                db.execute(delete_sql, (selected_doctor_id,))
                mysqldb.commit()
                sg.popup_ok(f"Doctor with ID {selected_doctor_id} deleted.")
                view_doctors_window.close()
                showViewDoctors()
                selected_doctor_id = None  # reset the selected ID after deletion

    return selected_doctor_id



def showBookAppointment():
    # select statements to retrieve patients and doctors
    db.execute("SELECT id, CONCAT(Salutation, ' ', First_Name, ' ', Surname) AS full_name FROM patients")
    patients_data = db.fetchall()
    patient_names = [f"{x[0]}: {x[1]}" for x in patients_data]

    db.execute("SELECT id, CONCAT(Salutation, ' ', First_Name, ' ', Surname) AS full_name FROM doctors")
    doctors_data = db.fetchall()
    doctor_names = [f"{x[0]}: {x[1]}" for x in doctors_data]
   

    appointmentLayout = [
        [sg.Text('Please enter the required details for a new appointment ' + version, font=16)],
        [sg.Text('Patient', size=(15, 1), font=14), sg.Combo(patient_names, key='-patientInfo-', font=14)],
        [sg.Text('Doctor', size=(15, 1), font=14), sg.Combo(doctor_names, key='-doctorInfo-', font=14)],
        [sg.Text('Department', size=(15, 1), font=14), sg.InputText(key='-appointmentDepartment-', font=14)],
        [sg.Text('Appointment Date', size=(15, 1), font=14), sg.InputText(key='-appointmentDate-', font=14)],
        [sg.Text('Appointment Time', size=(15, 1), font=14), sg.InputText(key='-appointmentTime-', font=14)],
        [sg.Button('Book Appointment'), sg.Button('Cancel')]
    ]

    bookAppointmentWindow = sg.Window('PMS Book Appointment ' + version, appointmentLayout)

    def bookAppointment(patient_info, doctor_info, department, appointment_date, appointment_time):
        # get patient_id and doctor_id from the selected combo box values
        patient_id = int(patient_info.split(':')[0])
        doctor_id = int(doctor_info.split(':')[0])

        # validation for empty fields
        if not patient_id or not doctor_id or not department or not appointment_date or not appointment_time:
            sg.popup_ok("Please fill in all required fields.")
            return

        # validation for date time formats
        try:
            datetime.strptime(appointment_date, '%Y-%m-%d')
            datetime.strptime(appointment_time, '%H:%M:%S')
        except ValueError:
            sg.popup_ok("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM:SS for time.")
            return

        sql = "INSERT INTO appointments(patient_id, doctor_id, department, appointment_date, appointment_time) VALUES (%s, %s, %s, %s, %s)"
        vals = patient_id, doctor_id, department, appointment_date, appointment_time
        db.execute(sql, vals)
        mysqldb.commit()
        print("Appointment booked for patient ", patient_id, " | " + patient_info + " with doctor ", str(doctor_id) + " | " + doctor_info + " at " + appointment_time + " on " + appointment_date)

    while True:
        event, values = bookAppointmentWindow.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            bookAppointmentWindow.close()
            break
        if event == "Book Appointment":
            bookAppointment(values['-patientInfo-'], values['-doctorInfo-'], values['-appointmentDepartment-'],
                            values['-appointmentDate-'], values['-appointmentTime-'])
            bookAppointmentWindow.close()

def showViewAppointments():
    selected_appointment_id = None

    db.execute("SELECT * FROM appointments")
    appointments_data = db.fetchall()

    appointment_layout = []
    headings = ['ID', 'Patient ID', 'Doctor ID', 'Department', 'Appointment Date', 'Appointment Time']
    data = [[str(appointment[0]), str(appointment[1]), str(appointment[2]), appointment[3], str(appointment[4]), str(appointment[5])] for appointment in appointments_data]

    view_appointments_layout = [
        [sg.Table(values=data, headings=headings, auto_size_columns=True, justification='right',
                  num_rows=min(25, len(data)), enable_events=True, key='-TABLE-',
                  col_widths=[5, 10, 10, 20, 20, 20],
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.Button('Change Details'), sg.Button('Delete Appointment'), sg.Button('Close')]
    ]

    view_appointments_window = sg.Window('View Appointments ' + version, view_appointments_layout)

    while True:
        event, values = view_appointments_window.read()

        if event == sg.WIN_CLOSED or event == 'Close':
            view_appointments_window.close()
            break

        if '-TABLE-' in event:
            row_index = values['-TABLE-'][0]
            # update selected array with selected record
            selected_appointment_id = data[row_index][0]

        if event == 'Change Details' and selected_appointment_id is not None:
            db.execute("SELECT * FROM appointments WHERE id = %s", (selected_appointment_id,))
            selected_appointment_data = db.fetchone()

            change_details_layout = [
                [sg.Text('Change Details', font=16)],
                [sg.Text('Department', size=(15, 1), font=14), sg.InputText(key='-changeAppointmentDepartment-', default_text=selected_appointment_data[3], font=14)],
                [sg.Text('Appointment Date', size=(15, 1), font=14), sg.InputText(key='-changeAppointmentDate-', default_text=str(selected_appointment_data[4]), font=14)],
                [sg.Text('Appointment Time', size=(15, 1), font=14), sg.InputText(key='-changeAppointmentTime-', default_text=str(selected_appointment_data[5]), font=14)],
                [sg.Button('Save Changes'), sg.Button('Cancel')]
            ]

            change_details_window = sg.Window('Change Appointment Details ' + version, change_details_layout)

            while True:
                change_event, change_values = change_details_window.read()

                if change_event == sg.WIN_CLOSED or change_event == 'Cancel':
                    change_details_window.close()
                    break

                if change_event == 'Save Changes':
                    update_sql = """
                        UPDATE appointments
                        SET department = %s, appointment_date = %s, appointment_time = %s
                        WHERE id = %s
                    """
                    update_vals = (
                        change_values['-changeAppointmentDepartment-'], change_values['-changeAppointmentDate-'],
                        change_values['-changeAppointmentTime-'], selected_appointment_id
                    )
                    db.execute(update_sql, update_vals)
                    mysqldb.commit()
                    sg.popup_ok("Appointment details updated successfully.")
                    change_details_window.close()
                    showViewAppointments()
                    

        if event == 'Delete Appointment' and selected_appointment_id is not None:
            confirm_delete = sg.popup_yes_no(f"Do you really want to delete appointment with ID {selected_appointment_id}?")
            if confirm_delete == 'Yes':
                delete_sql = "DELETE FROM appointments WHERE id = %s"
                db.execute(delete_sql, (selected_appointment_id,))
                mysqldb.commit()
                sg.popup_ok(f"Appointment with ID {selected_appointment_id} deleted.")
                change_details_window.close()
                showViewAppointments()
                selected_appointment_id = None # reset after delete

    return selected_appointment_id

db.execute('SELECT * FROM accounts')
for x in db:
    print(x)

db.execute("DELETE FROM accounts where username = ''")
mysqldb.commit()

db.execute('SELECT * FROM patients')
for x in db:
    print(x)

loginMethod()



