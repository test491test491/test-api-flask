#!/usr/bin/env python3

from app import app, bcrypt
from models import db, Fruit, VacationDestination

with app.app_context():
    Fruit.query.delete()
    VacationDestination.query.delete()

    apple = Fruit(name="apple")
    banana = Fruit(name="banana")

    ios_island = VacationDestination(name="Ios Island, Greece")
    santorini = VacationDestination(name="Santorini, Greece")

    db.session.add_all([apple, banana])
    db.session.add_all([ios_island, santorini])
    db.session.commit()
    
    print("🌱 Database successfully seeded! 🌱")