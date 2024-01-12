import sqlite3
DATABASE='customer_data.db'
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()
 


cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
            admin_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
            
        )''')

cursor.execute(''' 
    INSERT INTO admin (admin_id, name, email, password) values(9999990,'Manik', 'manik@tcs.com','Marvel@9')
''')

connection.commit()
connection.close()