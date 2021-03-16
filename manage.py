# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
from api import create_app
# from api.models import db

# sets up the app
app = create_app()
# manager = Manager(app)
# migrate = Migrate(app, db)

# @manager.command
# def runserver():
#     app.run(debug=True, host="0.0.0.0", port=5000)


# @manager.command
# def runworker():
#     app.run(debug=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
