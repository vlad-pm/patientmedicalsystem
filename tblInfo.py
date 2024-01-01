#tbl creation
tblAccountsColumns = """
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(20)
"""

tblPatientColumns = """
    id INT AUTO_INCREMENT PRIMARY KEY,
    Salutation VARCHAR(10) CHECK (Salutation IN ('Mr', 'Miss', 'Ms', 'Mrs', 'Mx')),
    First_Name VARCHAR(255) NOT NULL,
    Surname VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Phone_Number VARCHAR(20),
    First_Line_Address VARCHAR(255),
    Second_Line_Address VARCHAR(255),
    Town VARCHAR(255),
    PostCode VARCHAR(20)
"""
tblDoctorColumns = """
    id INT AUTO_INCREMENT PRIMARY KEY,
    Salutation VARCHAR(10) CHECK (Salutation IN ('Mr', 'Miss', 'Ms', 'Mrs', 'Mx')),
    First_Name VARCHAR(255) NOT NULL,
    Surname VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Department VARCHAR(255) NOT NULL
"""

tblAppointmentsColumns = """
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    department VARCHAR(255),
    appointment_date DATE,
    appointment_time TIME,
    FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
"""