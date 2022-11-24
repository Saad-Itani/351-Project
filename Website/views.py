from flask import Blueprint , render_template
#from . import app 
##### This is for defining a blueprint of our application which means it has  
## has a bunch of URLs defined in here . A way to seperate our app out   

views = Blueprint('views',__name__) ## attention to naming is unimportant, just by convention/ease ~ Saad
#app.register_blueprint(views, url_prefix='/')

@views.route('/', methods=['GET', 'POST']) ## GET and POST are Flask 

def home():
    return render_template("index.html")

@views.route('/rooms',methods=['GET','POST'])
def rooms():
    return render_template("rooms.html")