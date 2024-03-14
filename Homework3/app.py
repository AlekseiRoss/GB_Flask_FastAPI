from flask import Flask
from flask_wtf.csrf import CSRFProtect
from models import db

app = Flask(__name__)

app.config['SECRET_KEY'] = b'417ae6d173240862eeb649deb9a2f5bd795369e9117204401076e1a180219bb5'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True)
