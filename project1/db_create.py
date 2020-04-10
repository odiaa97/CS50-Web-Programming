import os
from flask import Flask, request, render_template
from model import *

app = Flask(__name__)

URI = "postgres://gqcymvpxhaebxl:864842868b216a580a752e84b29ea2eaccf3051c39c856a8f18c611241ab2252@ec2-23-21-160-38.compute-1.amazonaws.com:5432/d2qoamqonbficp"
app.config["SQLALCHEMY_DATABASE_URI"] = URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def main():
    # db.drop_all()
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        main()
