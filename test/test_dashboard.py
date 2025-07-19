import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from datetime import date, time, timedelta
from trackables import User, DailyEntry, WorkoutEntry
from database import Database

database = Database()

# Delete user if already exists
database.delete_user("John")

# Create test user
user = User("John", 170, 155, 2500)

database.insert_user(user)

# Generate 2 weeks of data
last_week_dates = [
    date(2025, 7, 7),   # Monday
    date(2025, 7, 8),   # Tuesday  
    date(2025, 7, 9),   # Wednesday
    date(2025, 7, 10),  # Thursday
    date(2025, 7, 11),  # Friday
    date(2025, 7, 12),  # Saturday
    date(2025, 7, 13),  # Sunday
]

for i, test_date in enumerate(last_week_dates):
    daily_entry = DailyEntry(
        test_date, 
        170 - i * 0.25,     # Weight: 170 to 168.5 lbs
        2000 + i * 50,      # Calories: 2000 to 2300 cal
        2800 + i * 200,     # Water: 2800 to 4000 mL
        8000 + i * 500,     # Steps: 8000 to 11000 steps
        7.0 + i * 0.2       # Sleep: 7.0 to 8.2 hours
    )
    database.insert_daily_entry("John", daily_entry)
    
    # Workout entries
    if i % 2 == 0:  # Every other day
        workout_entry = WorkoutEntry(
            test_date, 
            time(8, 0), 
            "Running",
            20 + i * 5,     # Minutes: 30 to 50
            "Moderate"
        )
        database.insert_workout_entry("John", workout_entry)

this_week_dates = [
    date(2025, 7, 14),  # Monday
    date(2025, 7, 15),  # Tuesday  
    date(2025, 7, 16),  # Wednesday
    date(2025, 7, 17),  # Thursday
    date(2025, 7, 18),  # Friday
    date(2025, 7, 19),  # Saturday
    date(2025, 7, 20),  # Sunday
]

for i, test_date in enumerate(this_week_dates):
    daily_entry = DailyEntry(
        test_date, 
        168.5 - i * 0.25,   # Weight: 168.5 to 167 lbs
        2000 + i * 25,      # Calories: 2000 to 2150 cal
        3000 + i * 250,     # Water: 3000 to 4500 mL
        10000 + i * 250,    # Steps: 10000 to 11500 steps
        7.5 + i * 0.25      # Sleep: 7.5 to 9 hours
    )
    database.insert_daily_entry("John", daily_entry)
    
    # More frequent workouts this week
    if i < 5:  # 5 out of 7 days
        workout_entry = WorkoutEntry(
            test_date, 
            time(15, 30), 
            "Weightlifting", 
            40 + i * 5,     # Minutes: 40 to 60
            "Moderate"
        )
        database.insert_workout_entry("John", workout_entry)

print("Success!")