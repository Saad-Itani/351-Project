from flask import Blueprint , render_template, request
from flask_mysqldb import MySQL
#from . import app 
##### This is for defining a blueprint of our application which means it has  
## has a bunch of URLs defined in here . A way to seperate our app out   

views = Blueprint('views',__name__) ## attention to naming is unimportant, just by convention/ease ~ Saad
#app.register_blueprint(views, url_prefix='/')

#configuredb
#views.config[MYSQL_HOST]='localhost'
#views.config[MYSQL_USER]='root'
#views.config[MYSQL_PASSWORD]='Leen@123456'
#views.config[MYSQL_DB]='flaskapp'
#mysql=MySQL(views)
@views.route('/', methods=['GET', 'POST']) ## GET and POST are Flask 

def home():
    return render_template("index.html")
''' @views.route('/',methods=['GET','POST'])
    def index()
    if request.method=='POST' #check whether post or get method 
        #fetch form data
        roomDetails=request.form
        CheckInDate=roomDetails['CheckInDate']
        CheckOutDate=roomDetails['CheckOutDate']
        RoomType=roomDetails['RoomType']
        RoomNumber=roomDetails['RoomNumber']
        cur= mysql.connection.cursor()
        cur.execute("INSERT INTO rooms(CheckInDate,CheckOutDate,RoomType,RoomNumber) VALUES(char,char,char,int)",(CheckInDate,CheckOutDate,RoomType,RoomNumber))
        mysql.connection.commit() #saves changes within our database-leen
        cur.close()
        return render_template("index.html")'''
#@views.route('/rooms',methods=['GET','POST'])
'''def rooms():
    #fetch details from database
    cur=mysql.connection.cursor()
    resultValue= cur.execute("SELECT * FROM rooms")
    if resultValue>0:
        roomDetails=cur.fetchall() # return all rows that have been fetched by mysql cursor -leen
        return render_template ('rooms.html',roomDetails=roomDetails)
    return render_template("rooms.html")
'''