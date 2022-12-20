from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# Add Databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret key!
app.config['SECRET_KEY'] = "arse_buscuits"
# initialise the Database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)

    # create string to display data
    def __repr__(self):
        return '<Name %r>' % self.name

# with app.app_context():
#     db.create_all()

#     db.session.add(Users(name="example 1", email = 'dermiemadsen@gmail.com'))
#     db.session.commit()

#     users = db.session.execute(db.select(Users)).scalars()


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("User name? ", validators=[DataRequired()])
    email = StringField("User email? ", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your name? ", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    return render_template("add_user.html")


@app.route('/')
def index():
    first_name = "Susan"
    last_name = "Parsons"
    middle_name = "Elizabeth"
    flash("Welcome to dermiesite!")

    favourite_pizza = ['pepperoni','Cheese','Mushroom','Shite']
    return render_template("index.html", first_name = first_name, last_name=last_name, middle_name=middle_name,
                        favourite_pizza = favourite_pizza)


@app.route('/user/<name>')

# def user(name):
#     return "<h1>Hello {}!!!</h1>".format(name)

def user(name):
    return render_template("user.html", user_name = name)

# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


# Create a Name Page
@app.route('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form submitted successfully!")
    return render_template("name.html", name=name, form=form)


if __name__ == '__main__':

   app.run()





