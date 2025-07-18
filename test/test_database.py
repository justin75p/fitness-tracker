import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from datetime import date, time, timedelta
from trackables import User, DailyEntry, WorkoutEntry
from database import Database

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

# -----------------------------------------------------------------------------------------------------------------------------------------------

# Test the new date range methods
user = User("TestUser", 125, 135, 2800)
database.insert_user(user)

# Insert a week's worth of entries
test_dates = [
    date(2025, 7, 7),   # Monday
    date(2025, 7, 8),   # Tuesday  
    date(2025, 7, 9),   # Wednesday
    date(2025, 7, 10),  # Thursday
    date(2025, 7, 11),  # Friday
    date(2025, 7, 12),  # Saturday
    date(2025, 7, 13),  # Sunday
]

for test_date in test_dates:
    daily_entry = DailyEntry(test_date, 125, 2800, 10000, 8)
    database.insert_daily_entry("TestUser", daily_entry)
    
    workout_entry = WorkoutEntry(test_date, time(12, 00), "Running", 30, "Moderate")
    database.insert_workout_entry("TestUser", workout_entry)

# Test getting the week's data
monday = date(2025, 7, 7)
daily_results = database.get_daily_entries_from_date("TestUser", monday, 7)
workout_results = database.get_workout_entries_from_date("TestUser", monday, 7)

print(f"Found {len(daily_results)} daily entries and {len(workout_results)} workout entries:")

for entry in daily_results:
    print(f"Daily Entry: {entry.entry_date}")

for entry in workout_results:
    print(f"Workout Entry: {entry.entry_date}")

database.delete_user("TestUser")