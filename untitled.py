import os
from flask import *
import mlab
from mongoengine import *
from werkzeug.utils import secure_filename

app = Flask(__name__)

mlab.connect()

app.config["IMG_PATH"] = os.path.join(app.root_path, "images")

class Ocean(Document):
    image = StringField()
    title = StringField()
    price = FloatField()

ocean1 = Ocean(image="https://s-media-cache-ak0.pinimg.com/736x/3e/ff/40/3eff4027c8fb613fa85e1277bf8108ac--blue-sunset-blue-ocean.jpg",
                title="Ocean 1",
                price=100000
                )
ocean1.save()

image = "https://s-media-cache-ak0.pinimg.com/736x/3e/ff/40/3eff4027c8fb613fa85e1277bf8108ac--blue-sunset-blue-ocean.jpg"
title = "Ocean 1"
price = 100000

oceans = [
    {
        "image":"https://s-media-cache-ak0.pinimg.com/736x/3e/ff/40/3eff4027c8fb613fa85e1277bf8108ac--blue-sunset-blue-ocean.jpg",
        "title":"Ocean 1",
        "price":100000
    },
    {
        "image": "https://www.blueoceanstrategy.com/wp-content/uploads/2015/01/What-is-blue-ocean-strategy.jpg",
        "title": "Ocean 2",
        "price": 200000
    },
    {
        "image": "https://sustainabledevelopment.un.org/content/images/image230_1231.jpg",
        "title": "Ocean 3",
        "price": 300000
    }
]


@app.route("/images/<image_name>")
def image(image_name):
    return send_from_directory(app.config["IMG_PATH"], image_name)

@app.route('/add-ocean', methods=["GET", "POST"])
def add_ocean():
    if request.method == "GET":
        return render_template("add_ocean.html")
    elif request.method == "POST":

        form = request.form
        title = form["title"]
        # image = form["image"]
        price = form["price"]

        image = request.files["image"]
        filename = secure_filename(image.filename)

        image.save(os.path.join(app.config["IMG_PATH"], filename))

        new_ocean = Ocean(title=title,
                          image="/images/{0}".format(filename),
                          price=price)
        new_ocean.save()
        return redirect(url_for("index"))

@app.route('/')
def index():
    return render_template("index.html",oceans=Ocean.objects())


@app.route("/about")
def about():
    return "hi, welcome to c4e10"

@app.route("/users/<username>")
def user(username):
    return "hello , my name is " + username

@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return "{0} + {1} = {2}".format(a, b, a + b)

if __name__ == '__main__':
    app.run()
