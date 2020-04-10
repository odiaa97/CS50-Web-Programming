import csv
from model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


DATABASE_URL = "postgres://gqcymvpxhaebxl:864842868b216a580a752e84b29ea2eaccf3051c39c856a8f18c611241ab2252@ec2-23-21-160-38.compute-1.amazonaws.com:5432/d2qoamqonbficp"

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


def main(csv_file):
    with open(f"{csv_file}", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            book = Book(title=row['title'], isbn=row['isbn'], author=row['author'], year=row['year'])
            db.add(book)
            db.commit()


if __name__ == "__main__":
    csv_path = "books.csv"
    main(csv_path)
