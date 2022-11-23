from flask import Blueprint , render_template

##### Similar to views file but this for the authentication (login page...)

auth = Blueprint('auth',__name__) ## attention to naming is unimportant, just by convention/ease 

#### Making routes for each login, logout , and signup and assigning dummy HTML headers for now* (20.11.2022 , 12:30 am) ~ Saad




@auth.route('/login', methods= ['GET', 'POST']) ## GET and POST are flask HTTP methods, where GET is used to retrieve information
def login():                                    ## from a web server, and POST is used to send information
    return render_template("login.html") ## referencing to the login page template 

@auth.route('/logout',  methods= ['GET', 'POST'])
def logout():
    return "<h1> Logout<h1>"

@auth.route('/signup', methods= ['GET', 'POST'])
def sign_up():
    return render_template("signUp.html")