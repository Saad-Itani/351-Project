from flask import Blueprint , render_template, render_template, request
from flask_mysqldb import MySQL
##### Similar to views file but this for the authentication (login page...)
#configure db
auth = Blueprint('auth',__name__) ## attention to naming is unimportant, just by convention/ease 
auth.config['MYSQL_HOST']='localhost'
auth.config['MYSQL_USER']='root'
auth.config['MYSQL_PASSWORD']='leen12345'
auth.config['MYSQL_DATABASE']='hotel_system'

#instaniate an object for this mysql model
mysql=MySQL(auth) # we can make use of this mysql object within our post request to make an entry into the database -leen
#### Making routes for each login, logout , and signup and assigning dummy HTML headers for now* (20.11.2022 , 12:30 am) ~ Saad




@auth.route('/login', methods= ['GET', 'POST'],methods=['GET','POST']) ## GET and POST are flask HTTP methods, where GET is used to retrieve information#identify this URL accepts post and get requests, if it is a GET request, we display the form to the user, if its a POST request we store the details onto the database -leen
def login():                                    ## from a web server, and POST is used to send information
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
    
    return render_template("login.html") ## referencing to the login page template 

@auth.route('/logout',  methods= ['GET', 'POST'])
def logout():
    return "<h1> Logout<h1>"

@auth.route('/signup', methods= ['GET', 'POST'])
def sign_up():
    return render_template("signUp.html")