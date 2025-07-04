import sqlite3
from datetime import date, timedelta
from trackables import User, DailyEntry, WorkoutEntry, WeeklySummary

class Database():
    def __init__(self):
        self.db_path = "fitness_data.db"
        self.create_tables()

    def create_tables(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        # User table
        user_table_query = """CREATE TABLE IF NOT EXISTS users(
            name TEXT,
            starting_weight REAL,
            goal_weight REAL,
            maintenance_calories INTEGER
        )"""
        cursor.execute(user_table_query)

        # Daily entry table
        daily_entry_table_query = """CREATE TABLE IF NOT EXISTS daily_entries(
            entry_date DATE PRIMARY KEY,
            weight REAL,
            calories INTEGER,
            steps INTEGER,
            sleep REAL 
        )"""
        cursor.execute(daily_entry_table_query)

        # Workout entry table
        workout_entry_table_query = """CREATE TABLE IF NOT EXISTS workout_entries(
            id INTEGER PRIMARY KEY,
            entry_date DATE,
            workout_type TEXT,
            minutes INTEGER,
            intensity TEXT
        )"""
        cursor.execute(workout_entry_table_query)

        connection.commit()
        connection.close()
        

