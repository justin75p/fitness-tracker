import sqlite3
from datetime import date, datetime, time, timedelta
from .trackables import User, DailyEntry, WorkoutEntry, WeeklySummary

class Database():
    # Constructor
    def __init__(self):
        self.db_path = "fitness_data.db"
        self.create_tables()
    
    # Helper method to create all necessary tables
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
            entry_date DATE,
            workout_time TIME,
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
        
    # Delete a user from user table
    def delete_user(self, name):


    # Insert a Daily Entry into the daily entries table
    def insert_daily_entry(self, daily_entry: DailyEntry):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        query = """
            INSERT INTO daily_entries(
                entry_date,
                weight,
                calories,
                steps,
                sleep
            )
            VALUES(
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """
        cursor.execute(query, (daily_entry.entry_date.strftime("%Y-%m-%d"), daily_entry.weight, daily_entry.calories, daily_entry.steps, daily_entry.sleep))

        connection.commit()
        connection.close()
    
    # Fetch daily entry from table
    def get_daily_entry(self, entry_date: date):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """SELECT * FROM daily_entries WHERE entry_date = (?)"""
        cursor.execute(query, (entry_date.strftime("%Y-%m-%d"),))

        output = cursor.fetchone()
        connection.close()

        if output:
            daily_entry = DailyEntry(datetime.strptime(output[0], "%Y-%m-%d").date(), output[1], output[2], output[3], output[4])
            return daily_entry
        
    # Delete a daily entry from daily entries table
    def delete_daily_entry(self, entry_date: date):


    # Insert a Workout Entry into the workout entries table
    def insert_workout_entry(self, workout_entry: WorkoutEntry):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """
                INSERT INTO workout_entries(
                    entry_date,
                    workout_time,
                    workout_type,
                    minutes,
                    intensity
                )
                VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """
        cursor.execute(query, (workout_entry.entry_date.strftime("%Y-%m-%d"), workout_entry.workout_time.strftime("%H:%M"),
                               workout_entry.workout_type, workout_entry.minutes, workout_entry.intensity))
            
        connection.commit()
        connection.close()

    # Fetch a workout entry using the entry date and workout time 
    def get_workout_entry(self, entry_date: date, workout_time: time):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """SELECT * FROM workout_entries WHERE entry_date = (?) AND workout_time = (?)"""
        cursor.execute(query, (entry_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))

        output = cursor.fetchone()
        connection.close()

        if output:
            workout_entry = WorkoutEntry(datetime.strptime(output[0], "%Y-%m-%d").date(), datetime.strptime(output[1], "%H:%M").time(),
                                         output[2], output[3], output[4])
            return workout_entry

    # Fetch all workout entries using the entry date
    def get_workout_entries_by_day(self, entry_date: date):
        # TODO: Implement method
        return None
    
    # Delete a workout entry using the entry date and workout time
    def delete_workout_entry(self, entry_date: date, workout_time: time):
        

            
        
