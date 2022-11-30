from flask import Flask, Blueprint , render_template, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from .auth import mysql
import MySQLdb.cursors

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
def reservation():
    if 'loggedin' in session:
        if request.method == "POST" :
            if "check-in" in request.form:
                if "check-out" in request.form:
                    check_in = request.form["check-in"]
                    check_out = request.form ["check-out"]
                    Email = session['username']
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("""SELECT DISTINCT r.room_num, r.price, r.room_type,
                                    FROM hotel AS h
                                    LEFT JOIN myroom AS r
                                        ON h.hotelID = r.hotelID
                                    ORDER BY r.room_num;""")

    result = cur.execute("SELECT hotel_name, FROM hotel WHERE room_num=%s", [room_num])
    cur.close()
    return render_template("rooms.html")

