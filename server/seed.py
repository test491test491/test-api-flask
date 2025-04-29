#!/usr/bin/env python3

from app import app, bcrypt
from models import db

with app.app_context():
    # Seed data goes here
    print("🌱 Database successfully seeded! 🌱")