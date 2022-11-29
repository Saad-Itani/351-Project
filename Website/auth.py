from flask import Flask, Blueprint , render_template, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from random import randint

##### Similar to views file but this for the authentication (login page...)



## Wanted to place the app in the __init__ folder but was confronted with the issue of circular imports :
app = Flask(__name__,template_folder='templates')## name of file/ or file run / this is how it initialized 
mysql = MySQL(app) # we can make use of this mysql object within our post request to make an entry into the database -leen

app.config['SECRET_KEY'] = 'saad'  ## encrypt or secure cookies and session data related to website (not important) ~ Saad
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Saad@123456'
app.config['MYSQL_DB'] = 'hotel_system'




auth = Blueprint('auth',__name__) ## attention to naming is unimportant, just by convention/ease 
#app.register_blueprint(auth, url_prefix='/') ## this is the prefix for all URLs stored in this blueprint file 

##mysql=MySQL(app) 



#### Making routes for each login, logout , and signup and assigning dummy HTML headers for now* (20.11.2022 , 12:30 am) ~ Saad


@auth.route('/login', methods= ['GET', 'POST']) ## GET and POST are flask HTTP methods, where GET is used to retrieve information#identify this URL accepts post and get requests, if it is a GET request, we display the form to the user, if its a POST request we store the details onto the database ~leen
def login():          
    msg = ''                          ## from a web server, and POST is used to send information
    if request.method == 'POST':
        if 'Email_address' in request.form:
            if 'password' in request.form:
                Email_address =  request.form['Email_address']
                password = request.form['password']
                with app.app_context():
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                    cursor.execute('SELECT * FROM users WHERE Email_address = % s AND  password = %s ', (Email_address,password))
                    account = cursor.fetchone()
                    if account:
                        session['loggedin']= True
                        session['id'] = account['ID']
                        session['username'] = account['First_Name']
                        msg = 'Logged in successfully !'
                        return render_template('index2.html', msg = msg) ## returns to the signed in page which includes logout and 
                    else:
                        msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
    
    @app.route('/')
    def Home():
        cur= mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        fetchdata = cur.fetchall()
        cur.close()
        
        return render_template('home.html',data=fetchdata)
    """
    if request.method='POST' #this means the submit button was hit from the form, and now we have the form data which needs to be stored onto the database -leen
    #fetch form data
    userDetails= request.form
    First_Name= userDetails['First_Name'] #stores name
    Last_Name=userDetails['Last_Name']
    ID= userDetails['ID']
    Password=userDetails['Password']
    Dob =userDetails['Dob']
    Balance =userDetails['name']
    Email_address=userDetails['Email_address'] #stores email , we need to store these values in the database to be able to use them - leen
    cursor = mysql.connection.cursor()
    cur.execute("INSERT INTO users(ID,First_Name,Last_Name,Password,Dob,Balance) VALUES ()")
    """
    return render_template("login.html") ## referencing to the login page template 

@auth.route('/logout',  methods= ['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template("logout.html")

@auth.route('/signup', methods= ['GET', 'POST'])
def sign_up():
    msg = " "
    if request.method == 'POST' :
       if 'First_Name' in  request.form and 'Last_Name' in request.form and 'Email_address' in request.form and 'password' in request.form:
        First_Name = request.form["First_Name"]
        Last_Name = request.form["Last_Name"]
        Email = request.form["Email_address"]
        password = request.form["password"] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Email_address = % s', [Email])
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            flash("Account already exists")
        else:
            id = randint(10000000,99999999) ## 9 digit id 
            cursor.execute('INSERT INTO users VALUES (%s, % s, % s, % s, %s, %s, %s)', (id, First_Name, Last_Name,Email,password,0,0 ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template("login.html",msg = msg)
    return render_template('signUp.html', msg = msg)


@auth.route('/resetpassword', methods= ['GET', 'POST'])
def reset_password():
    msg = " "
    if request.method == 'POST' :
       if  'Email_address' in request.form and 'password' in request.form:
        Email = request.form["Email_address"]
        password = request.form["password"] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Email_address = % s', [Email])
        account = cursor.fetchone()
       if not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            print("test2")
            msg = 'Invalid email address !'
         elif not Email or not password:
            print("test3")
            msg = 'Please fill out the form !'
        else:
            id = randint(10000000,99999999) ## 9 digit id 
            cursor.execute('INSERT INTO users VALUES (%s, % s, % s, % s, %s, %s, %s)', (id, First_Name, Last_Name,Email,password,0,0 ))
            mysql.connection.commit()
            msg = 'You have successfully changed your password !'
            return render_template("login.html",msg = msg)
    return render_template('resetPassword.html', msg = msg)
"""
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
