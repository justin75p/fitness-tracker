import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from datetime import date, time, timedelta
from trackables import User, DailyEntry, WorkoutEntry

# Test User class
user = User("Justin", 165, 155, 2700)
print(f"Name: {user.name}, Starting Weight: {user.starting_weight}, Goal Weight: {user.goal_weight}, Maintenance Calories: {user.maintenance_calories}")

# Test DailyEntry class
entry = DailyEntry(date.today(), 165, 2200, 3000, 10000, 8)
print(f"Daily Entry - Date: {entry.entry_date}, Weight: {entry.weight}, Calories: {entry.calories}, Water: {entry.water}, Steps: {entry.steps}, Sleep: {entry.sleep} hours")

# Test WorkoutEntry class
workout = WorkoutEntry(date.today(), time(16, 30), "Running", 30, "Moderate")
print(f"Workout - Date: {workout.entry_date}, Time: {workout.workout_time}, Type: {workout.workout_type}, Duration: {workout.minutes} min, Intensity: {workout.intensity}")