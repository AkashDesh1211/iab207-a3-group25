# This script imports the database instance and creates the database tables. 
from STEMWorkshops import db, create_app
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
quit()