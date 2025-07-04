import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import date
from src.trackables import User, DailyEntry, WorkoutEntry, WeeklySummary

# Test User class
user = User("Justin", 165, 155, 2700)
print(f"Name: {user.name}, Starting Weight: {user.starting_weight}, Goal Weight: {user.goal_weight}, Maintenance Calories: {user.maintenance_calories}")

# Test DailyEntry class
entry = DailyEntry(date.today(), 165, 2000, 10000, 8)
print(f"Daily Entry - Date: {entry.entry_date}, Weight: {entry.weight}, Calories: {entry.calories} Steps: {entry.steps}, Sleep: {entry.sleep} hours")

# Test WorkoutEntry class
workout = WorkoutEntry(date.today(), "Running", 30, "Moderate")
print(f"Workout - Type: {workout.workout_type}, Duration: {workout.minutes} min, Intensity: {workout.intensity}")

# Test WeeklySummary class
weekly = WeeklySummary(date.today())
print(f"Weekly Summary starting from {weekly.start_date}:")