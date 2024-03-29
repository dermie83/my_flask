from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# set FLASK_APP=hello.py
#### this initiates the db
# flask --app hello.py db init
#### this calls the migration
# flask --app hello.py db migrate


app = Flask(__name__)
# old sqlite3 db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# New Mysql db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password1234@localhost/our_users'
# Secret key!
app.config['SECRET_KEY'] = "arse_buscuits"
# initialise the Database
db = SQLAlchemy(app)
# migrate changes to app with db
migrate = Migrate(app, db)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    favourite_colour = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.now)
    # password stuff!
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # create string to display data
    def __repr__(self):
        return '<Name %r>' % self.name

# with app.app_context():
#     db.create_all()

#     db.session.add(Users(name="Dermie", email = 'dermiemadsen@gmail.com'))
#     db.session.commit()

#     users = db.session.execute(db.select(Users)).scalars()


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("User name ", validators=[DataRequired()])
    email = StringField("User email ", validators=[DataRequired()])
    favourite_colour = StringField("Favourite colour")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash_2', message="Password must match!")])
    password_hash_2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Delete Record
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    username = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", name=username,
                            form = form, 
                            our_users = our_users)
    except:
        flash("Whoops! There was a problem with deleting user, please try again...")
        return render_template("add_user.html", name=username,
                            form = form, 
                            our_users = our_users)


# Update Record
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = UserForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.favourite_colour = request.form['favourite_colour']
        try:
            db.session.commit()
            flash("User details updated successfully!")
            return render_template('update.html', 
            form = form, 
            user_to_update=user_to_update)
        except:
            flash("Error! Something went wrong, please try again...")
            return render_template('update.html', 
            form = form, 
            user_to_update=user_to_update)
    else:
        return render_template('update.html', 
            form = form, 
            user_to_update=user_to_update,
            id=id)


# Create a Form Class
class PasswordForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password_hash = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your name? ", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    username = None
    form = UserForm()
    # validate form
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            # Hash the password!!!
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data, 
                        favourite_colour=form.favourite_colour.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        username = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favourite_colour.data = ''
        form.password_hash.data = ''
        flash("User details added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", name=username,
                                            form = form, 
                                            our_users = our_users)


@app.route('/')
def index():
    first_name = "Susan"
    last_name = "Parsons"
    middle_name = "Elizabeth"
    flash("Welcome to dermiesite!")

    favourite_pizza = ['pepperoni','Cheese','Mushroom','Shite']
    return render_template("index.html", first_name = first_name, 
                                        last_name=last_name, 
                                        middle_name=middle_name,
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


# Create a password test Page
@app.route('/test_pw', methods = ['GET', 'POST'])
def test_pw():
    email = None
    password = None
    user_to_check = None
    passed = None
    form = PasswordForm()
    # validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ""
        form.password_hash.data = ""

        # Look up user by email address
        user_to_check = Users.query.filter_by(email=email).first()

        # Check Hashed Password
        passed = check_password_hash(user_to_check.password_hash, password)
        
    return render_template("test_pw.html", 
                            email=email, 
                            password=password, 
                            user_to_check = user_to_check,
                            passed = passed,
                            form=form)


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






