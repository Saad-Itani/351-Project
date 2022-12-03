from flask import Flask, Blueprint , render_template, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from .auth import mysql
import MySQLdb.cursors
from random import *
from datetime import datetime


#from . import app 
##### This is for defining a blueprint of our application which means it has  
## has a bunch of URLs defined in here . A way to seperate our app out   ~ Saad

views = Blueprint('views',__name__) ## attention to naming is unimportant, just by convention/ease ~ Saad
#app.register_blueprint(views, url_prefix='/')

########################## 

@views.route('/', methods=['GET', 'POST']) ## Displaying the homepage (not logged in ) ~ Saad
def home():
    return render_template("index.html")

@views.route('/invoice',methods=['GET', 'POST'])
def invoice():
    return render_template("invoices.html")

#####################################

@views.route('/reservation', methods = ['GET','POST'])

@views.route('/reservation', methods = ['GET','POST'])
def reservation():
    if 'loggedin' in session:
        if request.method == "POST" :
            if "checkin-date" in request.form:
                if "checkout-date" in request.form:
                    invoice = randint(10000000,99999999)
                    Email_address = session['username']
                    check_in = request.form['checkin-date']
                    check_out = request.form ['checkout-date']
                    room_num = request.form ['rooms']
                    room_type = request.form ['rooms']
                    checkin_date = datetime.datetime.strptime(check_in,'%m-%d-%Y') 
                    checkin_day = checkin_date.day
                    checkin_month = checkin_date.month
                    checkin_year = checkin_date.year
                    checkout_date = datetime.datetime.strptime(check_out,'%m-%d-%Y') 
                    checkout_day = checkin_date.day
                    checkout_month = checkin_date.month
                    checkout_year = checkin_date.year
                    days = 365*(checkout_year-checkin_year)+30*(checkout_month-checkin_month)+checkout_day-checkin_day
                    if days<0:
                            return render_template("rooms.html")
                    Balance = 129*days
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute('INSERT INTO reservation VALUES (%s, % s, % s, % s, %s, %s)', (invoice, Email_address, check_in,check_out,room_num, Balance))
                    cur.execute(''' FROM user
                                    LEFT JOIN reservation
                                        ON user.Balance = reservation.Balance;
                                    FROM user
                                    LEFT JOIN myroom
                                        ON user.Balance = reservation.Balance;
                                ''')
    cur.close()
    return render_template("index.html")


