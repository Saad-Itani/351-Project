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

@views.route('/invoice',methods=['GET', 'POST'])
def invoice():
    return render_template("invoices.html")