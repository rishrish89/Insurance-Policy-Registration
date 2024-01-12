#from crypt import methods
# from crypt import methods
from email import message
from email.policy import default
from re import S
from flask import Flask, render_template, request, redirect, url_for
import sqlite3


DATABASE='customer_data.db'
app = Flask(__name__)
# app.secret_key="Rishita"
lst1=[] 
name=[]
current_user=[]

# Function to initialize the SQLite database


def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            consumer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            address TEXT NOT NULL,
            contact TEXT NOT NULL,
            nominee_name TEXT NOT NULL,
            relationship TEXT
        )
    ''')
 
    connection.commit()
    connection.close()
 
# Initializing the database
init_db()
 
@app.route('/')
def registration_form():
    return render_template('Registration.html')
 
@app.route('/register', methods=['POST'])
def register():
    consumer_id = request.form['consumerId']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    contact = request.form['contact']
    nominee_name = request.form['nomineeName']
    relationship = request.form['nomineeRelation']
 
    connection = sqlite3.connect('customer_data.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT consumer_id FROM customers   WHERE consumer_id=?  ''', (consumer_id,))
    var10= cursor.fetchall()
    if var10:
        return render_template('registration.html')
    else:
        cursor.execute('''
            INSERT INTO customers (
                consumer_id, name, email, password, address, contact, nominee_name, relationship
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (consumer_id, name, email, password, address, contact, nominee_name, relationship))
        connection.commit()
        connection.close()
        lst1.append(consumer_id)
        lst1.append(name)
        lst1.append(email)
        return redirect(url_for('success_page'))
 
@app.route('/success')
def success_page():
    idd = lst1[0]
    name = lst1[1]
    email = lst1[2]
    lst1.clear()
    return render_template('acknowledgement.html', idk=idd, name = name, email= email)


def query_db(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = f"SELECT * FROM customers WHERE consumer_id=? AND password=?"
    cursor.execute(query, ((int(username)), password))
 
    user_data = cursor.fetchone()
    conn.close()
 
    return user_data


@app.route('/Login')
def login():
    # session['abc'] = 123
    current_user.clear()
    return render_template('Login.html')



@app.route('/login_Validation', methods=['GET', 'POST'])
def login_Validation():
    if request.method == 'POST' or request.method =='GET' :
        username = request.form['username']
        password = request.form['password']
    
        user_data = query_db(username, password)
        if user_data:
            name.clear()
            name.append(user_data[1])
            customerID=user_data[0]
            # session['abc'] = True
            return redirect(url_for('home', name=name[0],customerID=customerID))
        else:
            return render_template('invalid.html')
 
    return render_template('Login.html')

@app.route('/home')
def home():
    # print(session['abc'])
    # if 'abc' not in session or session['abc']== False:
    #     print('helooooo')
    #     return redirect('/Login')
    temp=request.args.get('customerID')
    current_user.append(temp)
    return render_template('Homepage.html', name=name[0])

# @app.route('/logout')
# def logout():
#     session.pop('abc',None)
#     # print(session['abc'])
#     return redirect('/Login')


@app.route('/PolicySelect')
def PolicySelect():
    return render_template('PolicySelect.html')

@app.route('/Policyaddition', methods=['POST'])
def Policyaddition():
    connection = sqlite3.connect('customer_data.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PolicySelect (
            policy_no INTEGER PRIMARY KEY AUTOINCREMENT,
            consumer_id INTEGER,
            commence_date DATE DEFAULT CURRENT_DATE,
            status VARCHAR(255) DEFAULT 'active',
            type VARCHAR(255),
            policy_title VARCHAR(255),
            premium_amount INT,
            next_due_date DATE DEFAULT (date('now', '+12 months')),
            sum_assured INT,
            policy_term INT,
            nominee_name VARCHAR(80) DEFAULT 'NA')
    ''')

    # print(current_user[0])
    type=request.form['policyType']
    policy_title=request.form['policyTitle']
    premium_amount=request.form['PremiumAmount']
    sum_assured=request.form['sumAssured']
    policy_term=request.form['PolicyTerms']
    nominee_name= request.form['nomineename']
    type1=''
    if type=='1':
        type1='General Insurance'
    elif type=='2':
        type1='Health Insurance'
    elif type=='3':
        type1='Motor Insurance'

    cursor.execute(''' SELECT nominee_name FROM customers WHERE consumer_id = ? ''',(current_user[0],))
    default_nominee = cursor.fetchall()
   


    if not nominee_name:
        cursor.execute(''' INSERT INTO PolicySelect (
            consumer_id, type, policy_title, premium_amount, sum_assured,policy_term,nominee_name)
             VALUES (?, ?, ?, ?, ?, ?, ?)''',(current_user[0],type1,policy_title,premium_amount,sum_assured,policy_term,default_nominee[0][0]))
    else:
        cursor.execute(''' INSERT INTO PolicySelect (
            consumer_id, type, policy_title, premium_amount, sum_assured,policy_term,nominee_name)
             VALUES (?, ?, ?, ?, ?, ?, ?)''',(current_user[0],type1,policy_title,premium_amount,sum_assured,policy_term,nominee_name))

    connection.commit()
    connection.close()
    return render_template('policySuccess.html')


def fetch_data(consumer_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
 
    # Fetch rows based on the provided consumer_id
    cursor.execute("SELECT * FROM PolicySelect WHERE consumer_id = ?", (consumer_id,))
    rows = cursor.fetchall()
 
    connection.close()
    return rows
 
@app.route('/ViewPolicy', methods=['GET', 'POST'])
def ViewPolicy():
    # if request.method == 'POST':
        # consumer_id = request.form['consumer_id']
        # if consumer_id != current_user[0]:
        #     return render_template('ViewPolicy.html', rows=None, message="You Don't have access to view other user policies")
        # else:   
        rows = fetch_data(current_user[0])
        if rows:
            return render_template('ViewPolicy.html', rows=rows)
        else:
            return render_template('ViewPolicy.html', rows=rows, message="Customer ID Not Found")
    
    # return render_template('ViewPolicy.html', rows=None)


@app.route('/changePassword', methods=['POST','GET'])
def changePassword():
    return render_template('changePassword.html')


@app.route('/updatePassword', methods=['POST','GET'])
def updatePassword():
    old = request.form['oldpass']
    newpass = request.form['cnfpass']
     
    connection = sqlite3.connect(DATABASE)
    print(current_user[0])
    cursor = connection.cursor()
    cursor.execute(''' SELECT password FROM customers WHERE consumer_id=?''',(current_user[0],))
    var2=cursor.fetchall()
    print(var2)

    if not var2[0][0]==old:
        return render_template('invalidpass.html')
    else:
        
        cursor.execute(''' UPDATE customers SET password =? WHERE consumer_id = ?''',(newpass,current_user[0]))
        connection.commit()
        connection.close()
        return render_template('pass_success.html')

@app.route('/delete')
def delete():
    rows = fetch_data(current_user[0])
    temp=request.args.get('message')
    if rows:
        return render_template('Deletepolicyuser.html', rows=rows,message=temp)
    else:
        return render_template('Deletepolicyuser.html', rows=rows, message="Customer ID Not Found")
    
    # return render_template('Deletepolicyuser.html')

@app.route('/delete_policy', methods=['POST'])
def delete_policy():

    try:
        policy_id = request.form['policyid']
 
        # Validate if policy_id exists in the database before deletion
        if policy_id:
            conn = sqlite3.connect('customer_data.db')
            cursor = conn.cursor()
 
            # Check if policy_id exists
            cursor.execute('SELECT * FROM policyselect WHERE policy_no = ? AND consumer_id=? ', (policy_id,current_user[0]))
            existing_policy = cursor.fetchone()
 
            if existing_policy:
                # Delete the policy
                cursor.execute('DELETE FROM policyselect WHERE policy_no = ?', (policy_id,))
                conn.commit()
                conn.close()
                message = f"Policy with ID {policy_id} deleted successfully."
            else:
                conn.close()
                message = f"Policy with ID {policy_id} not found."
 
        else:
            message = "Please provide a valid Policy ID."
 
    except Exception as e:
        message = f"An error occurred: {str(e)}"
 
    return redirect(url_for('delete', message=message))

@app.route('/admin')
def admin_login():
    current_user.clear()
    return render_template('AdminLogin.html')

def query_dba(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = f"SELECT * FROM admin WHERE admin_id=? AND password=?"
    cursor.execute(query, ((int(username)), password))
 
    user_data = cursor.fetchone()
    conn.close()
 
    return user_data

@app.route('/login_ValidationAdmin', methods=['GET', 'POST'])
def login_ValidationAdmin():
    if request.method == 'POST' or request.method =='GET' :
        username = request.form['username']
        password = request.form['password']
    
        user_data = query_dba(username, password)
        if user_data:
            name.clear()
            name.append(user_data[1])
            customerID=user_data[0]
            
            return redirect(url_for('Admin_home', name=name[0],customerID=customerID))
        else:
            return render_template('AdminLogin.html', message="**Invalid Credentials**")
 
    return render_template('AdminLogin.html')

@app.route('/Admin_home')
def Admin_home():
    temp=request.args.get('customerID')
    current_user.append(temp)
    return render_template('Admin_home.html',name=name[0])

@app.route('/admin_viewpolicy')
def admin_viewpolicy():
    return render_template('ViewPolicyAdmin.html')
def fetch_data1(consumer_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
 
    # Fetch rows based on the provided consumer_id
    cursor.execute("SELECT * FROM PolicySelect WHERE consumer_id = ?", (consumer_id,))
    rows = cursor.fetchall()
 
    connection.close()
    return rows
@app.route('/admin_view',methods=['GET','POST'])
def admin_view():
    if request.method == 'POST':
        consumer_id = request.form['consumer_id']
        
        rows = fetch_data1(consumer_id)
        if rows:
            return render_template('ViewPolicyAdmin.html', rows=rows)
        else:
            return render_template('ViewPolicyAdmin.html', rows=rows, message="Customer ID Not Found")
 
    return render_template('ViewPolicyAdmin.html', rows=None)


def fetch_data2():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
 
    cursor.execute("SELECT * FROM PolicySelect")
    rows = cursor.fetchall()
 
    connection.close()
    return rows
@app.route('/deleteadmin')
def deleteadmin():
    message= request.args.get('message')
    rows = fetch_data2()
    if rows:
        return render_template('deleteAdmin.html', rows=rows,message=message)
    else:
        return render_template('deleteAdmin.html', rows=rows, message="There are NO Policies to Display")
 


    # return render_template('deleteAdmin.html')

@app.route('/admin_delete',methods = ['GET','POST'])
def admin_delete():
    try:
        policy_id = request.form['policyid']
 
        # Validate if policy_id exists in the database before deletion
        if policy_id:
            conn = sqlite3.connect('customer_data.db')
            cursor = conn.cursor()
 
            # Check if policy_id exists
            cursor.execute('SELECT * FROM policyselect WHERE policy_no = ?', (policy_id,))
            existing_policy = cursor.fetchone()
 
            if existing_policy:
                # Delete the policy
                cursor.execute('DELETE FROM policyselect WHERE policy_no = ?', (policy_id,))
                conn.commit()
                conn.close()
                message = f"Policy with ID {policy_id} deleted successfully."
            else:
                conn.close()
                message = f"Policy with ID {policy_id} not found."
 
        else:
            message = "Please provide a valid Policy ID."
 
    except Exception as e:
        message = f"An error occurred: {str(e)}"
 
    return redirect(url_for('deleteadmin',message=message))

@app.route('/admin_policySelect')
def admin_policySelect():
    return render_template('PolicySelectAdmin.html')

@app.route('/adminPolicyaddition', methods=['POST'])
def adminPolicyaddition():
    connection = sqlite3.connect('customer_data.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PolicySelect (
            policy_no INTEGER PRIMARY KEY AUTOINCREMENT,
            consumer_id INTEGER,
            commence_date DATE DEFAULT CURRENT_DATE,
            status VARCHAR(255) DEFAULT 'active',
            type VARCHAR(255),
            policy_title VARCHAR(255),
            premium_amount INT,
            next_due_date DATE DEFAULT (date('now', '+12 months')),
            sum_assured INT,
            policy_term INT,
            nominee_name VARCHAR(80) DEFAULT 'NA')
    ''')


    # print(current_user[0])
    c_id=request.form['consumer_id']
    type=request.form['policyType']
    policy_title=request.form['policyTitle']
    premium_amount=request.form['PremiumAmount']
    sum_assured=request.form['sumAssured']
    policy_term=request.form['PolicyTerms']
    nominee_name= request.form['nomineename']
    type1=''
    if type=='1':
        type1='General Insurance'
    elif type=='2':
        type1='Health Insurance'
    elif type=='3':
        type1='Motor Insurance'

    cursor.execute(''' SELECT * FROM customers WHERE consumer_id = ? ''',(c_id,))
    temp3 = cursor.fetchall()
    if not temp3:
        return render_template('PolicySelectAdmin.html',message="Consumer ID Not Present")
    if not nominee_name:
        cursor.execute(''' INSERT INTO PolicySelect (
            consumer_id, type, policy_title, premium_amount, sum_assured,policy_term)
             VALUES (?, ?, ?, ?, ?, ?)''',(c_id,type1,policy_title,premium_amount,sum_assured,policy_term,))
    else:
        cursor.execute(''' INSERT INTO PolicySelect (
            consumer_id, type, policy_title, premium_amount, sum_assured,policy_term,nominee_name)
             VALUES (?, ?, ?, ?, ?, ?, ?)''',(c_id,type1,policy_title,premium_amount,sum_assured,policy_term,nominee_name))


    # cursor.execute(''' INSERT INTO PolicySelect (
    #         consumer_id, type, policy_title, premium_amount, sum_assured,policy_term)
    #          VALUES (?, ?, ?, ?, ?, ?)''',(c_id,type1,policy_title,premium_amount,sum_assured,policy_term,))
    
    connection.commit()
    connection.close()
    return render_template('policySuccessAdmin.html')


@app.route('/changePasswordAdmin', methods=['POST','GET'])
def changePasswordAdmin():
    return render_template('changePasswordAdmin.html')


@app.route('/updatePasswordAdmin', methods=['POST','GET'])
def updatePasswordAdmin():
    old = request.form['oldpass']
    newpass = request.form['cnfpass']
     
    connection = sqlite3.connect(DATABASE)
    print(current_user[0])
    cursor = connection.cursor()
    cursor.execute(''' SELECT password FROM admin WHERE admin_id=?''',(current_user[0],))
    var2=cursor.fetchall()

    if not var2[0][0]==old:
        return render_template('changePasswordAdmin.html', message="Wrong old Password")
    else:
        
        cursor.execute(''' UPDATE admin SET password =? WHERE admin_id = ?''',(newpass,current_user[0]))
        connection.commit()
        connection.close()
        return render_template('pass_successAdmin.html')
    





if __name__ == '__main__':
   app.run(debug=True)