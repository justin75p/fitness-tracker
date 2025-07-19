import os
import sqlite3
from datetime import date, datetime, time, timedelta
from trackables import User, DailyEntry, WorkoutEntry

class Database():
    # Constructor
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(project_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        
        self.db_path = os.path.join(data_dir, "fitness_data.db")
        self.create_tables()
    
    # Helper method to create all necessary tables
    def create_tables(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        # User table
        user_table_query = """CREATE TABLE IF NOT EXISTS users(
            user_name TEXT,
            starting_weight REAL,
            goal_weight REAL,
            maintenance_calories INTEGER
        )"""
        cursor.execute(user_table_query)

        # Daily entry table
        daily_entry_table_query = """CREATE TABLE IF NOT EXISTS daily_entries(
            user_name TEXT,
            entry_date DATE,
            weight REAL,
            calories INTEGER,
            water INTEGER,
            steps INTEGER,
            sleep REAL,
            PRIMARY KEY (user_name, entry_date)
        )"""
        cursor.execute(daily_entry_table_query)

        # Workout entry table
        workout_entry_table_query = """CREATE TABLE IF NOT EXISTS workout_entries(
            user_name TEXT,
            entry_date DATE,
            workout_time TIME,
            workout_type TEXT,
            minutes INTEGER,
            intensity TEXT,
            PRIMARY KEY (user_name, entry_date, workout_time)
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
                user_name,
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
    def get_user(self, user_name):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """SELECT * FROM users WHERE user_name = (?)"""
        cursor.execute(query, (user_name,))

        output = cursor.fetchone()
        connection.close()

        if output:
            user = User(output[0], output[1], output[2], output[3])
            return user
        
    # Retrieve a list of all user names
    def get_all_user_names(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """SELECT user_name FROM users"""
        cursor.execute(query)
        
        output = cursor.fetchall()

        user_name_list = [row[0] for row in output]

        return user_name_list


    # Update data related to User
    def update_user(self, user_name, new_name = None, new_start_weight = None, new_goal_weight = None, new_maintenance_calories = None):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        if new_start_weight:
            cursor.execute("""UPDATE users SET starting_weight = (?) WHERE user_name = (?)""", (new_start_weight, user_name))
        if new_goal_weight:
            cursor.execute("""UPDATE users SET goal_weight = (?) WHERE user_name = (?)""", (new_goal_weight, user_name))
        if new_maintenance_calories:
            cursor.execute("""UPDATE users SET maintenance_calories = (?) WHERE user_name = (?)""", (new_maintenance_calories, user_name))

        if new_name:
            cursor.execute("""UPDATE users SET user_name = (?) WHERE user_name = (?)""", (new_name, user_name))

        connection.commit()
        connection.close()

    # Delete a user from user table
    def delete_user(self, user_name):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """DELETE FROM users WHERE user_name = (?)"""
        cursor.execute(query, (user_name,))

        # Additionally, delete their related data
        query = """DELETE FROM daily_entries WHERE user_name = (?)"""
        cursor.execute(query, (user_name,))
        query = """DELETE FROM workout_entries WHERE user_name = (?)"""
        cursor.execute(query, (user_name,))

        connection.commit()
        connection.close()

    # Insert a Daily Entry into the daily entries table
    def insert_daily_entry(self, user_name: str, daily_entry: DailyEntry):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        query = """
            INSERT INTO daily_entries(
                user_name,
                entry_date,
                weight,
                calories,
                water,
                steps,
                sleep
            )
            VALUES(
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """
        cursor.execute(query, (user_name, daily_entry.entry_date.strftime("%Y-%m-%d"),
                               daily_entry.weight, daily_entry.calories, daily_entry.water, daily_entry.steps, daily_entry.sleep))

        connection.commit()
        connection.close()
    
    # Fetch daily entry from table
    def get_daily_entry(self, user_name:str, entry_date: date):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """SELECT * FROM daily_entries WHERE user_name = (?) AND entry_date = (?)"""
        cursor.execute(query, (user_name, entry_date.strftime("%Y-%m-%d")))

        output = cursor.fetchone()
        connection.close()

        if output:
            daily_entry = DailyEntry(datetime.strptime(output[1], "%Y-%m-%d").date(), output[2], output[3], output[4], output[5], output[6])
            return daily_entry
        
    # Fetch all daily entries from a specified date in a N day span
    def get_daily_entries_from_date(self, user_name: str, start_date: date, num_days):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        end_date = start_date + timedelta(days=num_days)
        query = """SELECT * FROM daily_entries WHERE user_name = (?) AND entry_date >= (?) AND entry_date < (?)"""

        cursor.execute(query, (user_name, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

        output = cursor.fetchall()
        connection.close()

        if output:
            daily_entries_list = []
            for row in output:
                if row:
                    daily_entries_list.append(DailyEntry(datetime.strptime(row[1], "%Y-%m-%d").date(), row[2], row[3], row[4], row[5], row[6]))
            return daily_entries_list
        return [] 
        
    # Update data related to a daily entry
    def update_daily_entry(self, user_name: str, entry_date: date, new_date: date = None, new_weight = None, new_calories = None, new_water = None, new_steps = None, new_sleep = None):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        if new_weight:
            cursor.execute("""UPDATE daily_entries SET weight = (?) WHERE user_name = (?) AND entry_date = (?)""", (new_weight, user_name, entry_date.strftime("%Y-%m-%d")))
        if new_calories:
            cursor.execute("""UPDATE daily_entries SET calories = (?) WHERE user_name = (?) AND entry_date = (?)""", (new_calories, user_name, entry_date.strftime("%Y-%m-%d")))
        if new_water:
            cursor.execute("""UPDATE daily_entries SET water = (?) WHERE user_name = (?) AND entry_date = (?)""", (new_water, user_name, entry_date.strftime("%Y-%m-%d")))
        if new_steps:
            cursor.execute("""UPDATE daily_entries SET steps = (?) WHERE user_name = (?) AND entry_date = (?)""", (new_steps, user_name, entry_date.strftime("%Y-%m-%d")))
        if new_sleep:
            cursor.execute("""UPDATE daily_entries SET sleep = (?) WHERE user_name = (?) AND entry_date = (?)""", (new_sleep, user_name, entry_date.strftime("%Y-%m-%d")))

        if new_date:
            cursor.execute("""UPDATE daily_entries SET entry_date = (?) WHERE user_name = (?) AND entry_date = (?)""", (new_date.strftime("%Y-%m-%d"), user_name, entry_date.strftime("%Y-%m-%d")))

        connection.commit()
        connection.close()

    # Delete a daily entry from daily entries table
    def delete_daily_entry(self, user_name:str, entry_date: date):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """DELETE FROM daily_entries WHERE user_name = (?) AND entry_date = (?)"""
        cursor.execute(query, (user_name, entry_date.strftime("%Y-%m-%d")))

        connection.commit()
        connection.close()

    # Insert a Workout Entry into the workout entries table
    def insert_workout_entry(self, user_name: str, workout_entry: WorkoutEntry):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """
                INSERT INTO workout_entries(
                    user_name,
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
                    ?,
                    ?
                )
                """
        cursor.execute(query, (user_name, workout_entry.entry_date.strftime("%Y-%m-%d"), workout_entry.workout_time.strftime("%H:%M"),
                               workout_entry.workout_type, workout_entry.minutes, workout_entry.intensity))
            
        connection.commit()
        connection.close()

    # Fetch a workout entry using the entry date and workout time 
    def get_workout_entry(self, user_name: str, entry_date: date, workout_time: time):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """SELECT * FROM workout_entries WHERE user_name = (?) AND entry_date = (?) AND workout_time = (?)"""
        cursor.execute(query, (user_name, entry_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))

        output = cursor.fetchone()
        connection.close()

        if output:
            workout_entry = WorkoutEntry(datetime.strptime(output[1], "%Y-%m-%d").date(), datetime.strptime(output[2], "%H:%M").time(),
                                         output[3], output[4], output[5])
            return workout_entry
    
    # Fetch all workout entries from a specified date in a N day span
    def get_workout_entries_from_date(self, user_name: str, start_date: date, num_days):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        end_date = start_date + timedelta(days=num_days)
        query = """SELECT * FROM workout_entries WHERE user_name = (?) AND entry_date >= (?) AND entry_date < (?)"""

        cursor.execute(query, (user_name, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

        output = cursor.fetchall()
        connection.close()

        if output:
            workout_entries_list = []
            for row in output:
                if row:
                    workout_entries_list.append(WorkoutEntry(datetime.strptime(row[1], "%Y-%m-%d").date(), datetime.strptime(row[2], "%H:%M").time(), row[3], row[4], row[5]))
            return workout_entries_list
        return [] 
    
    # Update data related to a workout entry
    def update_workout_entry(self, user_name: str, entry_date: date, workout_time: time, new_date: date = None, new_time: time = None, new_type = None, new_minutes = None, new_intensity = None):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        if new_type:
            cursor.execute("""UPDATE workout_entries SET workout_type = (?) WHERE user_name = (?) AND entry_date = (?) AND workout_time = (?)""",
                           (new_type, user_name, entry_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))
        if new_minutes:
            cursor.execute("""UPDATE workout_entries SET minutes = (?) WHERE user_name = (?) AND entry_date = (?) AND workout_time = (?)""",
                           (new_minutes, user_name, entry_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))
        if new_intensity:
            cursor.execute("""UPDATE workout_entries SET intensity = (?) WHERE user_name = (?) AND entry_date = (?) AND workout_time = (?)""",
                           (new_intensity, user_name, entry_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))

        if new_date and new_time:
            cursor.execute("""UPDATE workout_entries SET entry_date = (?) WHERE user_name = (?) AND entry_date = (?) AND workout_time = (?)""",
                           (new_date.strftime("%Y-%m-%d"), user_name, entry_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))
            cursor.execute("""UPDATE workout_entries SET workout_time = (?) WHERE user_name = (?) AND entry_date = (?) AND workout_time = (?)""",
                           (new_time.strftime("%H:%M"), user_name, new_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))
        elif new_date:
            cursor.execute("""UPDATE workout_entries SET entry_date = (?) WHERE user_name = (?) AND entry_date = (?) AND workout_time = (?)""",
                           (new_date.strftime("%Y-%m-%d"), user_name, entry_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))
        elif new_time:
            cursor.execute("""UPDATE workout_entries SET workout_time = (?) WHERE user_name = (?) AND entry_date = (?) AND workout_time = (?)""",
                           (new_time.strftime("%H:%M"), user_name, entry_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))

        connection.commit()
        connection.close()

    # Delete a workout entry using the entry date and workout time
    def delete_workout_entry(self, user_name: str, entry_date: date, workout_time: time):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        query = """DELETE FROM workout_entries WHERE user_name = (?) AND entry_date = (?) AND workout_time = (?)"""
        cursor.execute(query, (user_name, entry_date.strftime("%Y-%m-%d"), workout_time.strftime("%H:%M")))

        connection.commit()
        connection.close()

            
        
