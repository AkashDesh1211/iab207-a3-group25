from STEMWorkshops import create_app

# standard way to run the Flask app only if this file is executed directly
if __name__ == '__main__':
    app = create_app()
    #runs app
    app.run()