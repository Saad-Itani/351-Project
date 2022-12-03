##### Similar to views file but this for the authentication (login page...), this file contains the functions that concern with 
## user authentication such as signup, login, logout, user profile, ... ~ Saad 

### The importing of the required modules: 

from flask import Flask, Blueprint , render_template, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from random import randint
from flask import Flask, render_template, flash, redirect, request, url_for, session, g
from flask_mysqldb import MySQL



## Wanted to place the app in the __init__ folder but was confronted with the issue of circular imports :
app = Flask(__name__,template_folder='templates')## name of file/ or file run / this is how it initialized 
mysql = MySQL(app) # we can make use of this mysql object within our post request to make an entry into the database -leen

### making the connection with the database ~ Saad :  

app.config['SECRET_KEY'] = 'saad'  ## encrypt or secure cookies and session data related to website (not important) ~ Saad
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Saad@123456'
app.config['MYSQL_DB'] = 'hotel_system'

##########################


auth = Blueprint('auth',__name__) ## attention to naming is unimportant, just by convention/ease 
#app.register_blueprint(auth, url_prefix='/') ## this is the prefix for all URLs stored in this blueprint file 



## The auth.route defines the URL for each function/template and is crucial is redirecting, for example 
## the /login URL routes to the login function which opens the login template.  ~ Saad. 

####################### Login: 

@auth.route('/login', methods= ['GET', 'POST']) ## GET and POST are flask HTTP methods, where GET is used to retrieve information#identify this URL accepts post and get requests, if it is a GET request, we display the form to the user, if its a POST request we store the details onto the database ~leen
def login():                                    ## from a web server, and POST is used to send information
    msg = ''                          
    if request.method == 'POST':  ## We are checking if there is input on page ("POST")
        if 'Email_address' in request.form:  
            if 'password' in request.form:  ## Making sure both email and password are input
                Email_address =  request.form['Email_address']
                password = request.form['password']
                with app.app_context():   ## this was put in place due to an error in connecting to the database, however this fixed the issue ~ Saad
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) ## Cursor is how we interact with database (in SQL)
                    cursor.execute('SELECT * FROM users WHERE Email_address = % s AND  password = %s ', (Email_address,password)) 
                    account = cursor.fetchone() ## selecting everything from the users table of the row which belong to these info 
                    if account:
                        session['loggedin']= True
                        session['id'] = account['ID']
                        session['username'] = account["Email_address"]
                        msg = 'Logged in successfully !'
                        return render_template('index2.html', msg = msg) ## returns to the signed in page which includes logout and view profile
                    else:
                        msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
    
######################################################### ~ Saad


########################################  Logout: 

@auth.route('/logout',  methods= ['GET', 'POST'])
def logout():
    session.pop('loggedin', None) ## we are popping all these to indicate that the user is no longer 
    session.pop('id', None)       ## signed in so we are popping them (removing them ) ~ Saaad
    session.pop('username', None)
    return render_template("logout.html")

################################## ~ Saad

################################# Sign up: 

@auth.route('/signup', methods= ['GET', 'POST'])
def sign_up():
    msg = " "
    if request.method == 'POST' :  ## Similar to login 
       if 'First_Name' in  request.form and 'Last_Name' in request.form and 'Email_address' in request.form and 'password' in request.form:
        First_Name = request.form["First_Name"]
        Last_Name = request.form["Last_Name"]
        Email = request.form["Email_address"]
        password = request.form["password"] 
        Dob = request.form["Dob"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Email_address = % s', [Email]) 
        account = cursor.fetchone() ## we are checking if email already exists, then we give an error ~ Saad
        if account:
            msg = 'Account already exists !'
            flash("Account already exists")
        else:
            id = randint(10000000,99999999) ## Generating a random 9 digit ID ~ Saad
            cursor.execute('INSERT INTO users VALUES (%s, % s, % s, % s, %s, %s, %s)', (id, First_Name, Last_Name,Email,password,0,Dob ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template("login.html",msg = msg)
    return render_template('signUp.html', msg = msg)


@app.route('/login/profile') ## create the profile route and retrieve all the account details from the database only if the user is logged-in -leen
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        Email=session["username"]
        print(Email)
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Email_address = %s', [Email])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

####################################### Function to reset password if user forgot his password 

@app.route("/password_change", methods =['GET', 'POST'])
def password_change():
    message = ''
    if request.method == 'POST' :
        if'Email_address' in request.form and 'password' in request.form and 'confirm_password' in request.form  :
            password = request.form['password']   
            confirm_pass = request.form['confirm_password'] 
            Email = request.form['Email_address']
            if not password or not confirm_pass:
                message = 'Please fill out the form !'
            elif password != confirm_pass:
                message = 'Confirm password is not equal!' 
                flash ('Confirm password is not equal!')                
            else :
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    #updates password to the new password
                    cursor.execute('UPDATE users SET  password =% s WHERE Email_address =% s', (password, (Email, ), ))
                    mysql.connection.commit()
                    message = 'Password updated !' 
                    return render_template("login.html", msg = message)
    return render_template("resetPassword.html", msg = message)

############################################# ~ Saad and Leen 



@app.route("/edit", methods =['GET', 'POST'])
def edit():
    msg = ''    
    # Check if user is loggedin
    if 'loggedin' in session:
        editUserId = request.args.get('Email_address')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE ID = % s', (editUserId))
        editUser = cursor.fetchone()
        if request.method == 'POST' and 'First_Name' in request.form and 'Last_Name' in request.form and 'Password' in request.form and 'Email' in request.form:
            #new user info taken as inputs
            First_Name = request.form['First_Name']   
            Last_Name = request.form['Last_Name']
            Password = request.form['Password']            
            Email = request.form['Email_address']
            if not re.match(r'[A-Za-z0-9]+', First_Name):
                msg = 'name must contain only characters and numbers !'
            elif not re.match(r'[A-Za-z0-9]+', Last_Name):
                msg = 'name must contain only characters and numbers !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email_address):
                msg = 'Invalid email address !'
            elif request.method == 'POST':
                msg = 'Please fill out the form !'        
            else:
                #updates user info to the new inputs taken
                cursor.execute('UPDATE user SET   First_Name =% s, Last_Name =% s, Password =% s , WHERE Email_address =% s', (First_Name, Last_Name, Password, (Email, ), ))
                mysql.connection.commit()
                msg = 'User updated !'
                return redirect(url_for('users'))
        return render_template("edit.html", msg = msg, editUser = editUser)
        # User is not loggedin redirect to login page
    return redirect(url_for('login'))
