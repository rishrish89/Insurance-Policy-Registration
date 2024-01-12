import re
import sqlite3
import random
 
# SQLite database setup
conn = sqlite3.connect('Policy_database.db')
cursor = conn.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS Customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    email VARCHAR(30),
    password VARCHAR(30),
    address VARCHAR(100),
    contact_number VARCHAR(10),
    nominee_reg VARCHAR(5),
    nominee_name VARCHAR(50),
    relationship VARCHAR(50)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS PolicyMaster (
    policy_id INT PRIMARY KEY,
    policy_type VARCHAR(50),
    policy_title VARCHAR(100),
    start_date DATE,
    sum_assured DECIMAL(15, 2),
    premium DECIMAL(10, 2),
    paying_term INT
) ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS PolicyDetails (
    policy_issue_id INT PRIMARY KEY,
    customer_id INT,
    policy_id INT,
    policy_type VARCHAR(50),
    policy_title VARCHAR(100),
    premium DECIMAL(10,2),
    sum_assured DECIMAL(15, 2),
    policy_start_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    maturity_date DATE DEFAULT (date('now', '+2 years')),
    next_due_date DATE DEFAULT (date('now', '+6 months')),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (policy_id) REFERENCES PolicyMaster(policy_id)
) ''')

# cursor.execute('''INSERT INTO PolicyMaster (policy_id, policy_type, policy_title, start_date, sum_assured, premium, paying_term)
# VALUES
# (1000011, 'General Insurance', 'BimaGold', '2022-01-01', 50000.00, 1000.00, 10),
# (1000012, 'General Insurance', 'Janand', '2022-02-01', 75000.00, 1200.00, 12),
# (1000013, 'General Insurance', 'TravelSafe Assurance', '2022-03-01', 55000.00, 1200.00, 12),
# (1000014, 'General Insurance', 'BusinessGuard Shield', '2022-04-01', 70000.00, 1200.00, 12),
# (1000015, 'General Insurance', 'Vridhdhi', '2022-05-01', 100000.00, 1500.00, 15),
# (1000016, 'Health Insurance', 'Child Care','2022-01-01', 50000.00, 1000.00, 10),
# (1000017, 'Health Insurance', 'Family Wellness Plan','2022-01-01', 50000.00, 1000.00, 10),
# (1000018, 'Health Insurance', 'Senior Vitality Assurance','2022-01-01', 70000.00, 1000.00, 10),
# (1000019, 'Health Insurance', 'Mental Health Resilience','2022-01-01', 100000.00, 1000.00, 10),
# (1000020, 'Health Insurance', 'Personalized Wellness','2022-01-01', 75000.00, 1000.00, 10),
# (1000021, 'Motor Insurance', 'Roadside Assistance','2022-01-01', 50000.00, 1000.00, 10),
# (1000022, 'Motor Insurance', 'Rental Reimbursement Policy','2022-01-01', 75000.00, 1000.00, 10),
# (1000023, 'Motor Insurance', 'Personal Injury Protection (PIP)','2022-01-01', 85000.00, 1000.00, 10),
# (1000024, 'Motor Insurance', 'Floater','2022-01-01', 50000.00, 1000.00, 10),
# (1000025, 'Motor Insurance', 'Conventional','2022-01-01', 75000.00, 1000.00, 10)
# ''')

# conn.commit()

def check_password_strength(password):
    if len(password) < 8:
        print("Password should be at least 8 characters long.")
        return False
 
    if not any(char.isupper() for char in password):
        print("Password should contain at least one uppercase letter.")
        return False
 
    if not any(char.islower() for char in password):
        print("Password should contain at least one lowercase letter.")
        return False
    if not any(char.isdigit() for char in password):
       print("Password should contain at least one digit.")
       return False
 
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print("Password should contain at least one special character.")
        return False
 
    return True


class Customer:
    def __init__(self,CustomerId, CustomerName,email,password,address,ContactNumber,Nominee_reg, Nominee_Name,relation):
        self.CustomerId = CustomerId
        self.CustomerName =CustomerName
        self.email = email
        self.password=password
        self.address = address
        self.ContactNumber = ContactNumber
        self.Nominee_reg = Nominee_reg
        self.Nominee_Name =Nominee_Name
        self.relation = relation

    def save_to_database(self):
        cursor.execute('''
            INSERT INTO Customer VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (self.CustomerId, self.CustomerName, self.email, self.password, self.address, self.ContactNumber,self.Nominee_reg, self.Nominee_Name, self.relation))
        conn.commit()



def is_valid_email(email):
   
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_mobile_number(number):

    pattern = re.compile(r'^[6789]\d{9}$')
 
    if re.match(pattern, number):
        return True
    else:
        return False

def resgistration():
    customer_id=input("Enter Customer Id: ")
    while not customer_id.strip() or not customer_id.isdigit():
        if customer_id.isdigit()== False:
            print("Customer Id should be integer")
        else:    
            print("Input cannot be empty. Try again.")
        customer_id=input("Enter Customer Id: ")
            
          
    int(customer_id)

    customer_name=input("Enter Customer Name: ")




    while True:
        email=input("Enter Email: ")
        if is_valid_email(email):
            break
        else:
            print("Enter a valid email id.")

    while True:
            password=input("Enter Password: ")
            if not check_password_strength(password):
                password=input("Enter Password: ")
            else:
                break

    address = input("Enter Address: ")
    
    while True:
        mobile_number=input("Enter Mobile Number: ")
        if is_valid_mobile_number(mobile_number):
            break
        else:
            print("Enter a valid mobile number")

    Nominee_reg =""
    while True:
        check = input("Do You Want to add Nominee(y/n): ")
        if check.lower() == 'y':
            Nominee_reg = "Yes"
            Nominee_name = input("Enter Nominee Name: ")
            Relation = input("Enter Realationship with Nominee: ")
            break
        elif check.lower() == 'n':
            Nominee_reg = "No"
            Nominee_name = "NA"
            Relation = "NA"
            break
        else:
            print("Invalid Input")

    obj1 = Customer(customer_id,customer_name,email,password,address,mobile_number,Nominee_reg, Nominee_name,Relation)
    obj1.save_to_database()

    print("Customer Registration is Successful!")


def policy_selection():
    while True:
        customer_id=input("Enter Customer Id: ")
        while not customer_id.strip() or not customer_id.isdigit():
            if customer_id.isdigit()== False:
                print("Customer Id should be integer")
            else:    
                print("Input cannot be empty. Try again.")
            customer_id=input("Enter Customer Id: ")
                
            
        customer_id=int(customer_id)
        cursor.execute('''SELECT customer_id FROM Customer''')

        customer_ids = [row[0] for row in cursor.fetchall()]
        if customer_id in customer_ids:
            break
        else:
            print("Customer Not found")
 

    print("""
        Select Policy type From Below:
        [1] General Insurance
        [2] Health Insurance
        [3] Motor Insurance      
        
        """)

    while True:
        ip=input("Enter your Choice: ")
        if ip=='1' or ip=='2' or ip=='3':
            break
        else:
            print("Enter a Valid Option")
        
    if ip=='1':
        cursor.execute('''SELECT  policy_id,policy_title,sum_assured,premium,paying_term FROM  PolicyMaster WHERE policy_type= 'General Insurance' ''')
        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
 
        # Calculate column widths based on the length of the column names and maximum element in each column
        column_widths = [max(len(col), max(len(str(row[i])) for row in rows)) for i, col in enumerate(columns)]
        
        # Print the column headers
        for i, col in enumerate(columns):
            print(f"{col:<{column_widths[i]}}", end=' | ')
        print()
        
        # Print a separator line
        print("-" * (sum(column_widths) + len(column_widths) * 3 - 1))
        
        # Print each row in a formatted way
        for row in rows:
            for i, val in enumerate(row):
                print(f"{str(val):<{column_widths[i]}}", end=' | ')
            print()

        policy_type = "General Insurance"
        

    if ip=='2':
        cursor.execute('''  SELECT  policy_id,policy_title,sum_assured,premium,paying_term FROM  PolicyMaster WHERE policy_type= 'Health Insurance'  ''')
        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
 
        
        column_widths = [max(len(col), max(len(str(row[i])) for row in rows)) for i, col in enumerate(columns)]
        
        
        for i, col in enumerate(columns):
            print(f"{col:<{column_widths[i]}}", end=' | ')
        print()
        
        
        print("-" * (sum(column_widths) + len(column_widths) * 3 - 1))
        
        
        for row in rows:
            for i, val in enumerate(row):
                print(f"{str(val):<{column_widths[i]}}", end=' | ')
            print()

        policy_type = "Health Insurance"
        
        
    
    if ip=='3':
        cursor.execute('''  SELECT  policy_id,policy_title,sum_assured,premium,paying_term FROM  PolicyMaster WHERE policy_type= 'Motor Insurance'  ''')
        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
 
        
        column_widths = [max(len(col), max(len(str(row[i])) for row in rows)) for i, col in enumerate(columns)]
        
        
        for i, col in enumerate(columns):
            print(f"{col:<{column_widths[i]}}", end=' | ')
        print()
        
        
        print("-" * (sum(column_widths) + len(column_widths) * 3 - 1))
        
        
        for row in rows:
            for i, val in enumerate(row):
                print(f"{str(val):<{column_widths[i]}}", end=' | ')
            print()

        policy_type = "Motor Insurance"
        
        


    while True:
        PolicyId = input("Enter Policy Id: ")
        while not PolicyId.strip() or not PolicyId.isdigit():
            if PolicyId.isdigit()== False:
                print("Policy Id should be integer")
            elif len(PolicyId) != 7:
                print("PolicyId should be of 7 digit")
                PolicyId=input("Enter Policy Id: ")
            else:    
                print("Input cannot be empty. Try again.")
            PolicyId=input("Enter Policy Id: ")
        
        PolicyId=int(PolicyId)
        cursor.execute(''' SELECT policy_id FROM PolicyMaster ''')
        var = [row[0] for row in cursor.fetchall()]
        
        if PolicyId in var:
            break
        else:
            print("Enter a valid Policy ID")



    query = "SELECT policy_title, premium, sum_assured FROM PolicyMaster WHERE policy_id =?"
    cursor.execute(query, (PolicyId,))
    policy_title = cursor.fetchall()
    title = policy_title[0][0]
    pre = policy_title[0][1]
    sum_assure = policy_title[0][2]


    ran = random.randint(1000000,9999999)
    cursor.execute("INSERT INTO PolicyDetails (policy_issue_id, customer_id, policy_id,policy_type, policy_title,premium, sum_assured) VALUES (?,?,?,?,?,?,?)", (ran,customer_id,PolicyId,policy_type,title,pre, sum_assure))
    conn.commit()
    print("You have Succesfully Selected the Policy")


def view_policy():
    while True:
        customer_id=input("Enter Customer Id: ")
        while not customer_id.strip() or not customer_id.isdigit():
            if customer_id.isdigit()== False:
                print("Customer Id should be integer")
            else:    
                print("Input cannot be empty. Try again.")
            customer_id=input("Enter Customer Id: ")
                
            
        customer_id=int(customer_id)
        cursor.execute('''SELECT customer_id FROM Customer''')

        customer_ids = [row[0] for row in cursor.fetchall()]
        if customer_id in customer_ids:
            break
        else:
            print("Customer Not found")

    cursor.execute(''' SELECT p.policy_id, p.policy_start_date, c.customer_name, p.policy_type, p.policy_title, p.status, p.premium, p.sum_assured,c.nominee_reg, c.nominee_name, c.email, c.contact_number, p.next_due_date FROM Customer as c JOIN PolicyDetails as p ON c.customer_id = p.customer_id WHERE c.customer_id = ?''',(customer_id,))
    rows = cursor.fetchall()

    print("PolicyID | Date | CustomerName | Policy_Type | Policy_Title | Status | Premium | SumAssured |Nominee Registered ? | Nominee Name | Email | Phone Number | Due Date")
    print("-" * 100)
    
    # Print each row in a formatted way
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {row[9]} | {row[10]} | {row[11]} | {row[12]}")
        
    

    # columns = [desc[0] for desc in cursor.description]
 
    # # Set the maximum number of columns to display
    # max_columns_per_page = 5
    
    # # Calculate column widths based on the length of the column names and maximum element in each column
    # column_widths = [max(len(col), max(len(str(row[i])) for row in rows)) for i, col in enumerate(columns)]
    
    # # Calculate the number of pages based on the maximum number of columns per page
    # num_pages = -(-len(columns) // max_columns_per_page)  # Equivalent to math.ceil
    
    # # Set the maximum number of characters to display in a column
    # max_char_per_column = 20
    
    # # Define a function to print a formatted table for a given page
    # def print_table(page_num, start_col_idx, end_col_idx):
    #     page_columns = columns[start_col_idx:end_col_idx]
    #     page_column_widths = column_widths[start_col_idx:end_col_idx]
    
    #     # Print the column headers for the current page
    #     for i, col in enumerate(page_columns):
    #         print(f"{col[:max_char_per_column]:<{page_column_widths[i]}}", end=' | ')
    #     print()
    
    #     # Print a separator line
    #     print("-" * (sum(page_column_widths) + len(page_column_widths) * 3 - 1))
    
    #     # Print each row in a formatted way
    #     for row in rows[:5]:
    #         for i, val in enumerate(row[start_col_idx:end_col_idx]):
    #             print(f"{str(val)[:max_char_per_column]:<{page_column_widths[i]}}", end=' | ')
    #         print()
    
    # # Print each page
    # for page in range(1, num_pages + 1):
    #     start_col_idx = (page - 1) * max_columns_per_page
    #     end_col_idx = page * max_columns_per_page
    #     print_table(page, start_col_idx, end_col_idx)







    

if __name__ == '__main__':

    while True:
        print("""
-:Electricity Management System:- 
[1] Customer Registration
[2] Policy Selection
[3] View Policy Details
[0] Exit
Enter your Choice: """)

        option=int(input())
        if option==1:
            resgistration()
        elif option==2:
            policy_selection()

        elif option==3:
            view_policy()

        elif option==0:
            print("Exiting.....")
            break
        else:
            print("Invalid option. Please try again")

        check = input("Do you want to perform the operation again? (y/n): ")
        if check.lower() != 'y':
            temp= input("Are you sure want to exit (y/n): ")
            if temp!="n"or temp!= "n":
                break

conn.commit()
conn.close()






















