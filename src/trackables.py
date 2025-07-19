from datetime import date, time, timedelta

# User class containing starting weight, goal weight, and maintenance calories
class User():
    def __init__(self, name, starting_weight, goal_weight, maintenance_calories):
        self.name = name
        self.starting_weight = starting_weight
        self.goal_weight = goal_weight
        self.maintenance_calories = maintenance_calories

# Class to log weight, calories, steps and sleep daily
class DailyEntry():
    def __init__(self, entry_date: date, weight, calories, water, steps, sleep):
        self.entry_date = entry_date
        self.weight = weight
        self.calories = calories
        self.water = water
        self.steps = steps
        self.sleep = sleep

# Class to log workouts (type, duration and intensity)
class WorkoutEntry():
    def __init__(self, entry_date: date, workout_time: time, workout_type, minutes, intensity):
        self.entry_date = entry_date
        self.workout_time = workout_time
        self.workout_type = workout_type
        self.minutes = minutes
        self.intensity = intensity