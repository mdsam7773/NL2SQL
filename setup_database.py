import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker


conn = sqlite3.connect('clinic.db')
cursor = conn.cursor()


#create Tables

cursor.executescript("""
               
DROP TABLE IF EXISTS Patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS invoices;
               
               CREATE TABLE Patients (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT NOT NULL,
               last_name TEXT NOT NULL,
               email TEXT ,
               phone TEXT,
               date_of_birth DATE,
               gender TEXT ,
                city TEXT,
               registration_date DATE
               );
                     
                CREATE TABLE doctors (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     specialization TEXT,
                     department TEXT,
                     phone TEXT

                     );
                
                
                CREATE TABLE appointments ( 
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     patient_id INTEGER,
                     doctor_id INTEGER,
                     appointment_date DATETIME,
                     status TEXT,
                     notes TEXT,
                     FOREIGN KEY (patient_id) REFERENCES Patients(id),
                     FOREIGN KEY (doctor_id) REFERENCES doctors(id)
                     
                     );

                
                CREATE TABLE treatments (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     appointment_id INTEGER,
                     treatment_name TEXT,
                     cost REAL,
                     duration_minutes INTEGER,
                     foreign KEY (appointment_id) REFERENCES appointments(id)
                     
                     );

                CREATE TABLE invoices (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     patient_id INTEGER,
                     invoice_date DATE,
                     total_amount REAL,
                     paid_amount REAL,
                    due_amount REAL,
                     status TEXT,
                    FOREIGN KEY (patient_id) REFERENCES Patients(id)
                     );
                     

               """)


#insert doctors

specializations = ["Dermatology", "Cardiology", "Orthopedics", "General", "Pediatrics"]

fake = Faker()

for _ in range(15):
    cursor.execute("""
    INSERT INTO doctors (name, specialization, department, phone)
    VALUES (?, ?, ?, ?)
    """, (
        fake.name(),
        random.choice(specializations),
        "Dept " + str(random.randint(1, 5)),
        fake.phone_number()
    ))

# Insert patients
cities = ["Mumbai", "Delhi", "Nagpur", "Pune", "Indore", "Bhopal", "Jaipur", "Surat"]

for _ in range(200):
    cursor.execute("""
             INSERT INTO patients (first_name , last_name , email , phone , date_of_birth,
                   gender,city,registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   
                   """, (
                       fake.first_name(),
                       fake.last_name(),
                       fake.email() if random.random() > 0.2 else None,
                       fake.phone_number() if random.random() > 0.2 else None,
                       fake.date_of_birth(),
                       random.choice(["M","F"]),
                       random.choice(cities),
                       fake.date_between(start_date='-1y', end_date='today')
                   )
                   )

#insert appointments

statuses = ["Scheduled", "Completed", "Cancelled"]

for _ in range(500):
    cursor.execute("""

INSERT INTO appointments (patient_id, doctor_id , appointment_date, status, notes) 
                   VALUES (?, ?, ?, ?, ?)
                   """,
                   (random.randint(1,200),
                    random.randint(1,15),
                    fake.date_time_between(start_date='-1y', end_date='now'),
                    random.choice(statuses),
                    fake.text() if random.random() > 0.3 else None
                    
                    )
                   )

#insert treatments

for _ in range(350):
    cursor.execute("""
INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes) VALUES (?, ?, ?, ?)
                   
                   """,
                   (
                       random.randint(1,500),
                       fake.word(),
                       random.uniform(50,5000),
                       random.randint(10,120)
                   )
                   )

#insert invoices

invoice_statuses = ["Paid", "Pending", "Overdue"]

for _ in range(300):
    total = random.uniform(100, 10000)
    paid = total  if  random.random() > 0.3 else random.uniform(0,total)\
    
    cursor.execute(""" 

       INSERT INTO invoices (patient_id, invoice_date , total_amount,paid_amount, status)
                   VALUES (?, ?, ?, ?, ?)
""" ,  (
    random.randint(1,200),
    fake.date_between(start_date = '-1y', end_date = 'today'),
    total,
    paid,
    random.choice(invoice_statuses)
)
  )
    


conn.commit()
conn.close()