from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

# def index():
#     return ("Hellooo World!!!")

def index():
    first_name = "Susan"

    favourite_pizza = ['pepperoni','Cheese','Mushroom','Shite']
    return render_template("index.html", first_name = first_name,
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



if __name__ == '__main__':

   app.run()





