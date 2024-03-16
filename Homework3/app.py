from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from models import db, User
from forms import RegisterForm


app = Flask(__name__)

app.config['SECRET_KEY'] = b'417ae6d173240862eeb649deb9a2f5bd795369e9117204401076e1a180219bb5'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


def add_user(fname, lname, mail, passw):
    hashed_password = generate_password_hash(passw)
    user = User(first_name=fname, last_name=lname, email=mail,
                password=hashed_password)
    db.session.add(user)
    db.session.commit()


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        add_user(first_name, last_name, email, password)
        registered = True
    else:
        registered = False
    return render_template('register.html', form=form, registered=registered)


if __name__ == '__main__':
    app.run(debug=True)
