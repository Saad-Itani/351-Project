from flask import Flask, Blueprint , render_template, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
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
def login():                                    ## from a web server, and POST is used to send information
    
    if request.method == 'POST' and 'Email_address' in request.form and 'password' in request.form:
        Email_address =  request.form['Email_address']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM users WHERE Email_address = % s AND  password = %s ', (Email_address,password))
        account = cursor.fetchone()
        if account:
            return render_template("index.html", account = account)


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
    return "<h1> Logout<h1>"

@auth.route('/signup', methods= ['GET', 'POST'])
def sign_up():
    return render_template("signUp.html")