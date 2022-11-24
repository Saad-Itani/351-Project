from flask import Flask  # importing flask 
from .views import views  ## importing the blueprints
from .auth import auth, app ## importing the app 
from flask_mysqldb import MySQL ## importing to make the MYSQL connection

#app = Flask(__name__,template_folder='templates')## name of file/ or file run / this is how it initialized

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/') ## this is the prefix for all URLs stored in this blueprint file 







#app = create_app()