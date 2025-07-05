import sqlite3
from datetime import date, timedelta
from .trackables import User, DailyEntry, WorkoutEntry, WeeklySummary

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

    # Insert a user into the user table
    def insert_user(self, user: User):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        query = """
            INSERT INTO users(
                name,
                starting_weight,
                goal_weight,
                maintenance_calories
            )
            VALUES(
                ?,
                ?,
                ?,
                ?
            )"""
        cursor.execute(query, (user.name, user.starting_weight, user.goal_weight, user.maintenance_calories))

        connection.commit()
        connection.close()
    
    # Fetch user data from table
    def get_user(self, name):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """SELECT * FROM users WHERE name = (?)"""
        cursor.execute(query, (name,))

        output = cursor.fetchone()
        connection.close()

        if output:
            user = User(output[0], output[1], output[2], output[3])
            return user

    # Insert a Daily Entry into the daily entries table
    def insert_daily_entry(self, daily_entry: DailyEntry):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

    # Insert a Workout Entry into the workout entries table
    def insert_workout_entry(self, workout_entry: WorkoutEntry):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()


            
        
