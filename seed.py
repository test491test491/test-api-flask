#!/usr/bin/env python3

from app import app, bcrypt
from models import db, Fruit

with app.app_context():
    Fruit.query.delete()

    apple = Fruit(name="apple")
    banana = Fruit(name="banana")

    db.session.add_all([apple, banana])
    db.session.commit()
    
    print("🌱 Database successfully seeded! 🌱")