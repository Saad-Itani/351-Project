from Website.templates import create_app 

app = create_app() 

if __name__ == '__main__':  ## this means only if we run this file, not if we import this file we are going to excute
    app.run(debug=True) ## run our  flask application, and start a webserver, debug = True means 
                                ## every time we change our python code it is going to automatically rerun 
                                # the webserver 
                                # We want this off when we finish and are in production ~ Saad
    
    