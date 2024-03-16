from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.secret_key = ' key'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/charity management system'
db= SQLAlchemy(app)

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'charity management system'
mysql=MySQL(app)
# Intialize MySQL
@app.route('/')
def hello_world():
    try:
        charitymanagementsystem .query.all()
        return 'connected'
    except:
        return 'not connected'
        
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    print(request.method)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email_id = % s AND password = % s', (username, password, ))
        login = cursor.fetchone()
        print(login)
        if login:
            session['loggedin'] = True
            session['id'] = login['id']
            session['username'] = login['email_id']
            msg = 'Logged in successfully !'
            return render_template('homepage.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))
app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'register' in request.form: #'email_id' in request.form and 'password' in request.form and 'full_name' in request.form and 'gender' in request.form and 'address_1' in request.form and 'address_2' in request.form and 'district' in request.form and 'State' in request.form and 'country' in request.form and 'phone_no' in request.form and 'DOB' in request.form and 'Occupation' in request.form and 'role_details' in request.form :
        email_id = request.form['email_id']
        password = request.form['password']
        full_name = request.form['full_name']
        gender = request.form['gender']
        address_1 = request.form['address_1']
        address_2 = request.form['address_2']
        district = request.form['district']
        State = request.form['State']
        country = request.form['country']
        phone_no = request.form['phone_no']
        DOB = request.form['DOB']
        Occupation = request.form['Occupation']
        role_details = request.form['role_details']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email_id = % s AND password = % s AND Full_name = % s ', (email_id,full_name, ))
        user = cursor.fetchone()
        if user:
            msg = 'user already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', full_name):
            msg = 'Username must contain only characters and numbers !'
        elif not full_name or not password or not email_id:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (%s, % s, % s, % s, % s, % s, % s, % s, % s, % i % s, % s)', (email_id, password, full_name,gender,address_1,address_2,district,State,country,Occupation,DOB,phone_no,Occupation,role_details ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
if __name__ == '__main__':
    app.run(debug=True)