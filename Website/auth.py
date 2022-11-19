from flask import Blueprint 

##### Similar to views file but this for the authentication (login page...)

auth = Blueprint('auth',__name__) ## attention to naming is unimportant, just by convention/ease 

#### Making routes for each login, logout , and signup and assigning dummy HTML headers for now* (20.11.2022 , 12:30 am) ~ Saad

@auth.route('/login')
def login():
    return "<h1>login<h1>"

@auth.route('/logout')
def logout():
    return "<h1> Logout<h1>"

@auth.route('/signup')
def sign_up():
    return "<h1>Sign Up<h1>"