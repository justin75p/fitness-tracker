import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import date, timedelta
from src.trackables import User, DailyEntry, WorkoutEntry, WeeklySummary
from src.database import Database

database = Database()

# Test insertion and retrieval of a User
user = User("Andy", 150, 160, 2500)

database.insert_user(user)
outputted_user = database.get_user("Andy")

print(f"Name: {outputted_user.name}, Starting Weight: {outputted_user.starting_weight}, Goal Weight: {outputted_user.goal_weight}, Maintenance Calories: {outputted_user.maintenance_calories}")


