import sys
import mysql.connector
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QTabWidget, QMessageBox, QComboBox, QGroupBox)

class HospitalManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospital Management System")
        self.setGeometry(100, 100, 900, 600)
        
        # Connect to MySQL database
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vanshika271438",
            database="hospital12"
        )
        self.create_tables()
        
        self.setup_ui()
        
    def create_tables(self):
        cursor = self.db_connection.cursor()
        try:
            # Patients table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT,
                    gender VARCHAR(20),
                    address VARCHAR(200),
                    phone VARCHAR(20),
                    emergency_contact VARCHAR(20),
                    blood_group VARCHAR(10)
                )
            """)
            
            # Doctors table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    specialization VARCHAR(100),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    department VARCHAR(50)
                )
            """)
            
            # Appointments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT,
                    doctor_id INT,
                    date DATE,
                    time VARCHAR(20),
                    status VARCHAR(20),
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            """)
            
            self.db_connection.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()
    
    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Add tabs
        tabs.addTab(self.create_patient_tab(), "Patients")
        tabs.addTab(self.create_doctor_tab(), "Doctors")
        tabs.addTab(self.create_appointment_tab(), "Appointments")
        
        # Initialize tables
        self.refresh_patient_table()
        self.refresh_doctor_table()
        self.refresh_appointment_table()
        
    def create_patient_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Form group
        form_group = QGroupBox("Patient Information")
        form_layout = QVBoxLayout()
        form_group.setLayout(form_layout)
        
        # Fields
        self.patient_fields = {
            
            'name': QLineEdit(),
            'age': QLineEdit(),
            'gender': QComboBox(),
            'address': QLineEdit(),
            'phone': QLineEdit(),
            'emergency_contact': QLineEdit(),
            'blood_group': QComboBox()
        }
        
        self.patient_fields['gender'].addItems(["Male", "Female", "Other"])
        self.patient_fields['blood_group'].addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        # Add fields to form
        fields = ["Name", "Age", "Gender", "Address", "Phone", "Emergency Contact", "Blood Group"]
        for i, key in enumerate(self.patient_fields):
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(fields[i] + ":"))
            hbox.addWidget(self.patient_fields[key])
            form_layout.addLayout(hbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Patient")
        add_button.clicked.connect(self.add_patient)
        update_button = QPushButton("Update Patient")
        update_button.clicked.connect(self.update_patient)
        delete_button = QPushButton("Delete Patient")
        delete_button.clicked.connect(self.delete_patient)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_patient_fields)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)
        
        # Table
        self.patient_table = QTableWidget()
        
        # Add widgets to layout
        layout.addWidget(form_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.patient_table)
        
        return tab
    
    def create_doctor_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Form group
        form_group = QGroupBox("Doctor Information")
        form_layout = QVBoxLayout()
        form_group.setLayout(form_layout)
        
        # Fields
        self.doctor_fields = {
            'name': QLineEdit(),
            'specialization': QLineEdit(),
            'phone': QLineEdit(),
            'email': QLineEdit(),
            'department': QComboBox()
        }
        
        self.doctor_fields['department'].addItems([
            "Cardiology", "Neurology", "Orthopedics", 
            "Pediatrics", "General Medicine", "Surgery"
        ])
        
        # Add fields to form
        fields = ["Name", "Specialization", "Phone", "Email", "Department"]
        for i, key in enumerate(self.doctor_fields):
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(fields[i] + ":"))
            hbox.addWidget(self.doctor_fields[key])
            form_layout.addLayout(hbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Doctor")
        add_button.clicked.connect(self.add_doctor)
        update_button = QPushButton("Update Doctor")
        update_button.clicked.connect(self.update_doctor)
        delete_button = QPushButton("Delete Doctor")
        delete_button.clicked.connect(self.delete_doctor)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_doctor_fields)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)
        
        # Table
        self.doctor_table = QTableWidget()
        
        # Add widgets to layout
        layout.addWidget(form_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.doctor_table)
        
        return tab
    
    def create_appointment_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Form group
        form_group = QGroupBox("Appointment Information")
        form_layout = QVBoxLayout()
        form_group.setLayout(form_layout)
        
        # Fields
        self.appointment_fields = {
            'patient_id': QComboBox(),
            'doctor_id': QComboBox(),
            'date': QLineEdit(),
            'time': QComboBox(),
            'status': QComboBox()
        }
        
        self.appointment_fields['time'].addItems([
            "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
            "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM"
        ])
        
        self.appointment_fields['status'].addItems(["Scheduled", "Completed", "Cancelled"])
        
        # Add fields to form
        fields = ["Patient", "Doctor", "Date (YYYY-MM-DD)", "Time", "Status"]
        for i, key in enumerate(self.appointment_fields):
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(fields[i] + ":"))
            hbox.addWidget(self.appointment_fields[key])
            form_layout.addLayout(hbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Appointment")
        add_button.clicked.connect(self.add_appointment)
        update_button = QPushButton("Update Appointment")
        update_button.clicked.connect(self.update_appointment)
        delete_button = QPushButton("Delete Appointment")
        delete_button.clicked.connect(self.delete_appointment)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_appointment_fields)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)
        
        # Table
        self.appointment_table = QTableWidget()
        
        # Add widgets to layout
        layout.addWidget(form_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.appointment_table)
        
        return tab
    
    # Patient CRUD operations
    def add_patient(self):
        cursor = self.db_connection.cursor()
        try:
            query = """
                INSERT INTO patients (name, age, gender, address, phone, emergency_contact, blood_group)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                self.patient_fields['name'].text(),
                int(self.patient_fields['age'].text()),
                self.patient_fields['gender'].currentText(),
                self.patient_fields['address'].text(),
                self.patient_fields['phone'].text(),
                self.patient_fields['emergency_contact'].text(),
                self.patient_fields['blood_group'].currentText()
            )
            cursor.execute(query, values)
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Patient added successfully!")
            self.refresh_patient_table()
            self.refresh_patient_combobox()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding patient: {e}")
        finally:
            cursor.close()
    
    def update_patient(self):
        selected_items = self.patient_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a patient to update")
            return
            
        patient_id = selected_items[0].text()
        cursor = self.db_connection.cursor()
        try:
            query = """
                UPDATE patients SET 
                name = %s, age = %s, gender = %s, address = %s, 
                phone = %s, emergency_contact = %s, blood_group = %s
                WHERE patient_id = %s
            """
            values = (
                self.patient_fields['name'].text(),
                int(self.patient_fields['age'].text()),
                self.patient_fields['gender'].currentText(),
                self.patient_fields['address'].text(),
                self.patient_fields['phone'].text(),
                self.patient_fields['emergency_contact'].text(),
                self.patient_fields['blood_group'].currentText(),
                patient_id
            )
            cursor.execute(query, values)
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Patient updated successfully!")
            self.refresh_patient_table()
            self.refresh_patient_combobox()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating patient: {e}")
        finally:
            cursor.close()
    
    def delete_patient(self):
        selected_items = self.patient_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a patient to delete")
            return
            
        patient_id = selected_items[0].text()
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete patient ID {patient_id}?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
                self.db_connection.commit()
                QMessageBox.information(self, "Success", "Patient deleted successfully!")
                self.refresh_patient_table()
                self.refresh_patient_combobox()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting patient: {e}")
            finally:
                cursor.close()
    
    def clear_patient_fields(self):
        for field in self.patient_fields.values():
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)
    
    def refresh_patient_table(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT * FROM patients")
            patients = cursor.fetchall()
            
            self.patient_table.setRowCount(len(patients))
            self.patient_table.setColumnCount(8)
            self.patient_table.setHorizontalHeaderLabels([
                "Patient ID", "Name", "Age", "Gender", "Address", 
                "Phone", "Emergency Contact", "Blood Group"
            ])
            
            for row_num, patient in enumerate(patients):
                for col_num, data in enumerate(patient):
                    self.patient_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
                    
            self.patient_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error refreshing patient table: {e}")
        finally:
            cursor.close()
    
    # Doctor CRUD operations
    def add_doctor(self):
        cursor = self.db_connection.cursor()
        try:
            query = """
                INSERT INTO doctors (name, specialization, phone, email, department)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                self.doctor_fields['name'].text(),
                self.doctor_fields['specialization'].text(),
                self.doctor_fields['phone'].text(),
                self.doctor_fields['email'].text(),
                self.doctor_fields['department'].currentText()
            )
            cursor.execute(query, values)
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Doctor added successfully!")
            self.refresh_doctor_table()
            self.refresh_doctor_combobox()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding doctor: {e}")
        finally:
            cursor.close()
    
    def update_doctor(self):
        selected_items = self.doctor_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a doctor to update")
            return
            
        doctor_id = selected_items[0].text()
        cursor = self.db_connection.cursor()
        try:
            query = """
                UPDATE doctors SET 
                name = %s, specialization = %s, phone = %s, email = %s, department = %s
                WHERE doctor_id = %s
            """
            values = (
                self.doctor_fields['name'].text(),
                self.doctor_fields['specialization'].text(),
                self.doctor_fields['phone'].text(),
                self.doctor_fields['email'].text(),
                self.doctor_fields['department'].currentText(),
                doctor_id
            )
            cursor.execute(query, values)
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Doctor updated successfully!")
            self.refresh_doctor_table()
            self.refresh_doctor_combobox()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating doctor: {e}")
        finally:
            cursor.close()
    
    def delete_doctor(self):
        selected_items = self.doctor_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a doctor to delete")
            return
            
        doctor_id = selected_items[0].text()
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete doctor ID {doctor_id}?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))
                self.db_connection.commit()
                QMessageBox.information(self, "Success", "Doctor deleted successfully!")
                self.refresh_doctor_table()
                self.refresh_doctor_combobox()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting doctor: {e}")
            finally:
                cursor.close()
    
    def clear_doctor_fields(self):
        for field in self.doctor_fields.values():
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)
    
    def refresh_doctor_table(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT * FROM doctors")
            doctors = cursor.fetchall()
            
            self.doctor_table.setRowCount(len(doctors))
            self.doctor_table.setColumnCount(6)
            self.doctor_table.setHorizontalHeaderLabels([
                "Doctor ID", "Name", "Specialization", 
                "Phone", "Email", "Department"
            ])
            
            for row_num, doctor in enumerate(doctors):
                for col_num, data in enumerate(doctor):
                    self.doctor_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
                    
            self.doctor_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error refreshing doctor table: {e}")
        finally:
            cursor.close()
    
    # Appointment CRUD operations
    def add_appointment(self):
        cursor = self.db_connection.cursor()
        try:
            query = """
                INSERT INTO appointments (patient_id, doctor_id, date, time, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                self.appointment_fields['patient_id'].currentData(),
                self.appointment_fields['doctor_id'].currentData(),
                self.appointment_fields['date'].text(),
                self.appointment_fields['time'].currentText(),
                self.appointment_fields['status'].currentText()
            )
            cursor.execute(query, values)
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Appointment added successfully!")
            self.refresh_appointment_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding appointment: {e}")
        finally:
            cursor.close()
    
    def update_appointment(self):
        selected_items = self.appointment_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select an appointment to update")
            return
            
        appointment_id = selected_items[0].text()
        cursor = self.db_connection.cursor()
        try:
            query = """
                UPDATE appointments SET 
                patient_id = %s, doctor_id = %s, date = %s, time = %s, status = %s
                WHERE appointment_id = %s
            """
            values = (
                self.appointment_fields['patient_id'].currentData(),
                self.appointment_fields['doctor_id'].currentData(),
                self.appointment_fields['date'].text(),
                self.appointment_fields['time'].currentText(),
                self.appointment_fields['status'].currentText(),
                appointment_id
            )
            cursor.execute(query, values)
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Appointment updated successfully!")
            self.refresh_appointment_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating appointment: {e}")
        finally:
            cursor.close()
    
    def delete_appointment(self):
        selected_items = self.appointment_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select an appointment to delete")
            return
            
        appointment_id = selected_items[0].text()
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete appointment ID {appointment_id}?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("DELETE FROM appointments WHERE appointment_id = %s", (appointment_id,))
                self.db_connection.commit()
                QMessageBox.information(self, "Success", "Appointment deleted successfully!")
                self.refresh_appointment_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting appointment: {e}")
            finally:
                cursor.close()
    
    def clear_appointment_fields(self):
        for field in self.appointment_fields.values():
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)
    
    def refresh_appointment_table(self):
        cursor = self.db_connection.cursor()
        try:
            query = """
                SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name, 
                a.date, a.time, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
            """
            cursor.execute(query)
            appointments = cursor.fetchall()
            
            self.appointment_table.setRowCount(len(appointments))
            self.appointment_table.setColumnCount(6)
            self.appointment_table.setHorizontalHeaderLabels([
                "Appointment ID", "Patient Name", "Doctor Name", 
                "Date", "Time", "Status"
            ])
            
            for row_num, appointment in enumerate(appointments):
                for col_num, data in enumerate(appointment):
                    self.appointment_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
                    
            self.appointment_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error refreshing appointment table: {e}")
        finally:
            cursor.close()
    
    # Combo box refresh methods
    def refresh_patient_combobox(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT patient_id, name FROM patients")
            patients = cursor.fetchall()
            
            self.appointment_fields['patient_id'].clear()
            for patient_id, name in patients:
                self.appointment_fields['patient_id'].addItem(f"{name} (ID: {patient_id})", patient_id)
        except Exception as e:
            print(f"Error refreshing patient combobox: {e}")
        finally:
            cursor.close()
    
    def refresh_doctor_combobox(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT doctor_id, name, specialization FROM doctors")
            doctors = cursor.fetchall()
            
            self.appointment_fields['doctor_id'].clear()
            for doctor_id, name, specialization in doctors:
                self.appointment_fields['doctor_id'].addItem(
                    f"Dr. {name} ({specialization}) (ID: {doctor_id})", 
                    doctor_id
                )
        except Exception as e:
            print(f"Error refreshing doctor combobox: {e}")
        finally:
            cursor.close()
    
    def showEvent(self, event):
        self.refresh_patient_combobox()
        self.refresh_doctor_combobox()
        super().showEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HospitalManagementSystem()
    window.show()
    sys.exit(app.exec_())