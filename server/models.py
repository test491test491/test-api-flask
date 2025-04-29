from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# contains definitions of tables and associated schema constructs
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# define a model class by inheriting from db.Model
class Fruit(db.Model, SerializerMixin):
    __tablename__ = "fruits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    @validates('name')
    def validate_name(self, column_name, value):
        if type(value) != str:
            raise TypeError(f"{column_name} must be a string!")
        elif len(value) < 5:
            raise ValueError(f"{column_name} must be at least 5 characters long!")
        else:
            return value