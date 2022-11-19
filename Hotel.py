
### This is for test*   ~ Saad


from flask import Flask 
#import flask_mysqldb
class Hotel:
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Hello this is main page"

    if __name__ == "__main__":
        app.run()