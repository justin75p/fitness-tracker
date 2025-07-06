import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import date, time, timedelta
from src.trackables import User, DailyEntry, WorkoutEntry, WeeklySummary
from src.database import Database

database = Database()

# Test insertion and retrieval of a User
user = User("Andy", 150, 160, 2500)

database.insert_user(user)
outputted_user = database.get_user("Andy")

print(f"Name: {outputted_user.name}, Starting Weight: {outputted_user.starting_weight}, Goal Weight: {outputted_user.goal_weight}, Maintenance Calories: {outputted_user.maintenance_calories}")

# Test insertion and retrieval of a Daily Entry
daily_entry = DailyEntry(date(2025, 7, 4), 150, 2500, 8000, 7.5)

database.insert_daily_entry("Andy", daily_entry)
outputted_entry = database.get_daily_entry("Andy", date(2025, 7, 4))

print(f"Daily Entry - Date: {outputted_entry.entry_date}, Weight: {outputted_entry.weight}, Calories: {outputted_entry.calories} Steps: {outputted_entry.steps}, Sleep: {outputted_entry.sleep} hours")

# Test removal of a Daily Entry
database.delete_daily_entry("Andy", date(2025, 7, 4))
outputted_entry = database.get_daily_entry("Andy", date(2025, 7, 4))
if not outputted_entry:
    print("No Daily Entry Found.\n")

# Test insertion and retrieval of a Workout Entry
workout_entry = WorkoutEntry(date(2025, 7, 4), time(15, 30), "Running", 60, "Moderate")

database.insert_workout_entry("Andy", workout_entry)
outputted_workout_entry = database.get_workout_entry("Andy", date(2025, 7, 4), time(15, 30))

print(f"Workout - Date: {outputted_workout_entry.entry_date}, Time: {outputted_workout_entry.workout_time}, Type: {outputted_workout_entry.workout_type}, Duration: {outputted_workout_entry.minutes} min, Intensity: {outputted_workout_entry.intensity}")

# TODO: Test retrieval of Workout Entry on a day with multiple workouts

# Test removal of a Workout Entry
database.delete_workout_entry("Andy", date(2025, 7, 4), time(15, 30))
outputted_workout_entry = database.get_workout_entry("Andy", date(2025, 7, 4), time(15, 30))
if not outputted_workout_entry:
    print("No Workout Entry Found.\n")

# Test removal of a User
database.delete_user("Andy")
outputted_user = database.get_user("Andy")
if not outputted_user:
    print("No user found.\n")