from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = "arse_buscuits"

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your name? ", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')

# def index():
#     return ("Hellooo World!!!")

def index():
    first_name = "Susan"
    last_name = "Parsons"
    middle_name = "Elizabeth"

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
    return render_template("name.html")


if __name__ == '__main__':

   app.run()





