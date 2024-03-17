from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.secret_key = ' key'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/charity_management_system'
db= SQLAlchemy(app)

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'charity_management_system'
mysql=MySQL(app)


#Table to store adopters info 
class adoption( db.Model):
    Adoption_id = db.Column(db.Integer, primary_key=True)
    Adopter_id = db.Column(db.Integer, unique=True)
    Orphanage_Oldage_id = db.Column(db.Integer)
    Child_id = db.Column(db.Integer)
    Requested_date = db.Column(db.String(50), nullable=False)
    Adopted_Date = db.Column(db.String(50), nullable=False)
    
# Table to store clothes donation info 
class cloth_box(db.Model):
    donation_id = db.Column(db.Integer, primary_key=True)
    donar_id = db.Column(db.Integer, unique=True)
    orphanage_oldage_id = db.Column(db.Integer, unique=True)
    age_group = db.Column(db.Integer)
    cloth_desc = db.Column(db.String(1000))
    donation_requested_date = db.Column(db.String(50), nullable=False)
    donated_date = db.Column(db.String(50), nullable=False)

# Table to select country  
class country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(20))  

# Table to select district  
class district(db.Model):
    dist_id = db.Column(db.Integer, primary_key=True)
    dist_name = db.Column(db.String(20))

# Table to store event details 
class event_details(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(20))

# Table to store event organization details 
class event_organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, unique=True)
    orphanage_oldage_id = db.Column(db.Integer, unique=True)
    event_type = db.Column(db.Integer, unique=True)
    anticipated_date = db.Column(db.String(50), nullable=False)
    approved_date = db.Column(db.String(50), nullable=False)
    no_of_approved_hours = db.Column(db.String(50), nullable=False)
    no_of_anticipated_hours = db.Column(db.String(50), nullable=False)
    anticipated_guest = db.Column(db.String(50), nullable=False)
    approved_guest = db.Column(db.String(50), nullable=False)

# Table to store food donation details 
class food_support(db.Model):
    Donation_id = db.Column(db.Integer, primary_key=True)
    Donar_id = db.Column(db.Integer, unique=True)
    orphanage_oldage_id = db.Column(db.Integer, unique=True)
    Food_description = db.Column(db.String(1000))
    Total_Quantity = db.Column(db.Integer)
    Donation_Requested_date = db.Column(db.String(50), nullable=False)
    Donated_Date = db.Column(db.String(50), nullable=False)

# Table to store fund details 
class funding(db.Model):
    Donation_id = db.Column(db.Integer, primary_key=True)
    Donar_id = db.Column(db.Integer, unique=True)
    orphanage_oldage_id = db.Column(db.Integer, unique=True)
    Funding_Amount = db.Column(db.Integer)
    Donation_Requested_date = db.Column(db.String(50), nullable=False)
    Donated_Date = db.Column(db.String(50), nullable=False)

# Table to store occupation details 
class occupation(db.Model):
    occupation_id = db.Column(db.Integer, primary_key=True)
    occupation_name = db.Column(db.String(20))

# Table to store orphanage and oldage details  
class orphanage_oldage_details(db.Model):
    orphanage_oldage_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    address_1 = db.Column(db.String(20))
    address_2 = db.Column(db.String(20))
    district = db.Column(db.Integer, unique=True)
    state = db.Column(db.Integer, unique=True)
    country = db.Column(db.Integer, unique=True)
    tresurer = db.Column(db.Integer, unique=True)
    warden = db.Column(db.Integer, unique=True)
    director = db.Column(db.Integer, unique=True)
    phone_no = db.Column(db.Integer)
    email_id = db.Column(db.String(20))
    website = db.Column(db.String(20))

# Table to store people details 
class people_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orphanage_oldage_id = db.Column(db.Integer, unique=True)
    Full_name = db.Column(db.String(20))
    Age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    Class = db.Column(db.Integer)

# Table to select state  
class state(db.Model):
    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(20))

# Table to store user details 
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(20))
    password = db.Column(db.String(20))
    Full_name = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    address_1 = db.Column(db.String(20))
    address_2 = db.Column(db.String(20))
    district = db.Column(db.Integer, unique=True)
    state = db.Column(db.Integer, unique=True)
    country = db.Column(db.Integer, unique=True)
    phone_no = db.Column(db.Integer)
    DOB = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.Integer, unique=True)
    

# Intialize MySQL


# Customer can login
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

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/register', methods =['GET','POST'])
def register():
    print("Regiser")
    msg = ''
    if request.method == 'POST' and 'register' in request.form: #'email_id' in request.form and 'password' in request.form and 'full_name' in request.form and 'gender' in request.form and 'address_1' in request.form and 'address_2' in request.form and 'district' in request.form and 'State' in request.form and 'country' in request.form and 'phone_no' in request.form and 'DOB' in request.form and 'Occupation' in request.form and 'role_details' in request.form :
        email_id = request.form['email_id']
        password = request.form['password']
        full_name = request.form['full_name']
        gender = request.form['gender']
        address_1 = request.form['address_1']
        address_2 = request.form['address_2']
        district = request.form['district']
        State = request.form['state']
        country = request.form['country']
        phone_no = request.form['phone_no']
        DOB = request.form['DOB']
        Occupation = request.form['occupation']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM users WHERE email_id = % s ', (email_id ))
        user = users.query.filter_by(email_id=email_id).first()
        if user:
            flash(f"An account with Email {email_id} already exists", "warning")
            return render_template('/register.html')
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
    # return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)