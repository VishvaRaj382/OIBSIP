"""
Professional Database Storage Module for BMI Calculator
Handles SQLite data persistence, multi-user profiles, statistical summaries,
CSV exports, Clinical Text Report exports, historical records, and error logging.
"""

import sqlite3
import csv
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional


class DatabaseError(Exception):
    """Custom Exception for Database Operations."""
    pass


class DatabaseManager:
    def __init__(self, db_path: str = "bmi_tracker.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        """Helper to create sqlite connection with timeout."""
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to connect to database at {self.db_path}: {e}")

    def _init_db(self):
        """Initialize SQLite database tables if they do not exist."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        created_at TEXT NOT NULL
                    )
                """)
                
                # Create bmi_records table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bmi_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        weight_kg REAL NOT NULL,
                        height_m REAL NOT NULL,
                        bmi_value REAL NOT NULL,
                        category TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                    )
                """)
                
                # Ensure default user 'Default User' exists
                cursor.execute("SELECT id FROM users WHERE name = ?", ("Default User",))
                if not cursor.fetchone():
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("INSERT INTO users (name, created_at) VALUES (?, ?)", ("Default User", now))
                    
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Database initialization failed: {e}")

    def get_all_users(self) -> List[Dict]:
        """Fetch all user profiles."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, created_at FROM users ORDER BY id ASC")
                rows = cursor.fetchall()
                return [{"id": row["id"], "name": row["name"], "created_at": row["created_at"]} for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Error fetching users: {e}")

    def get_or_create_user(self, name: str) -> Dict:
        """Fetch user by name, creating if new."""
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("User name cannot be empty.")
            
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, created_at FROM users WHERE LOWER(name) = LOWER(?)", (clean_name,))
                row = cursor.fetchone()
                
                if row:
                    return {"id": row["id"], "name": row["name"], "created_at": row["created_at"]}
                else:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("INSERT INTO users (name, created_at) VALUES (?, ?)", (clean_name, now))
                    user_id = cursor.lastrowid
                    conn.commit()
                    return {"id": user_id, "name": clean_name, "created_at": now}
        except sqlite3.Error as e:
            raise DatabaseError(f"Error getting/creating user '{clean_name}': {e}")

    def add_bmi_record(self, user_id: int, weight_kg: float, height_m: float, bmi_value: float, category: str) -> int:
        """Insert a new BMI measurement record."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO bmi_records (user_id, weight_kg, height_m, bmi_value, category, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, weight_kg, height_m, round(bmi_value, 2), category, now))
                record_id = cursor.lastrowid
                conn.commit()
                return record_id
        except sqlite3.Error as e:
            raise DatabaseError(f"Error saving BMI record: {e}")

    def get_user_history(self, user_id: int) -> List[Dict]:
        """Fetch all BMI history for a specific user ordered chronologically."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, weight_kg, height_m, bmi_value, category, timestamp
                    FROM bmi_records
                    WHERE user_id = ?
                    ORDER BY id ASC
                """, (user_id,))
                rows = cursor.fetchall()
                return [{
                    "id": row["id"],
                    "weight_kg": row["weight_kg"],
                    "height_m": row["height_m"],
                    "bmi_value": row["bmi_value"],
                    "category": row["category"],
                    "timestamp": row["timestamp"]
                } for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Error fetching user history: {e}")

    def get_user_stats(self, user_id: int) -> Dict:
        """Calculates summary statistics for a user's BMI history."""
        records = self.get_user_history(user_id)
        if not records:
            return {
                "total_records": 0,
                "latest_bmi": None,
                "latest_weight": None,
                "weight_change": 0.0,
                "min_bmi": None,
                "max_bmi": None,
                "avg_bmi": None
            }

        bmis = [r["bmi_value"] for r in records]
        weights = [r["weight_kg"] for r in records]
        initial_weight = weights[0]
        latest_weight = weights[-1]
        weight_change = latest_weight - initial_weight

        return {
            "total_records": len(records),
            "latest_bmi": bmis[-1],
            "latest_weight": latest_weight,
            "weight_change": round(weight_change, 1),
            "min_bmi": min(bmis),
            "max_bmi": max(bmis),
            "avg_bmi": round(sum(bmis) / len(bmis), 2)
        }

    def export_user_history_to_csv(self, user_id: int, file_path: str) -> str:
        """Export a user's historical records to a CSV file."""
        records = self.get_user_history(user_id)
        if not records:
            raise ValueError("No historical records available to export.")

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Record ID", "Timestamp", "Weight (kg)", "Height (m)", "BMI Value", "Category"])
                for r in records:
                    writer.writerow([r["id"], r["timestamp"], r["weight_kg"], r["height_m"], r["bmi_value"], r["category"]])
            return file_path
        except IOError as e:
            raise DatabaseError(f"Failed to export CSV file: {e}")

    def export_clinical_report_txt(self, user_id: int, user_name: str, file_path: str) -> str:
        """Export a formatted Clinical Health Report text document."""
        records = self.get_user_history(user_id)
        stats = self.get_user_stats(user_id)
        if not records:
            raise ValueError("No records available to generate report.")

        try:
            with open(file_path, mode='w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write(f"           CLINICAL HEALTH & BMI ANALYTICS REPORT\n")
                f.write("=" * 70 + "\n\n")
                f.write(f" Patient Name    : {user_name}\n")
                f.write(f" Report Date     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f" Total Logged    : {stats['total_records']} measurements\n")
                f.write(f" Latest BMI      : {stats['latest_bmi']:.2f}\n")
                f.write(f" Net Weight Delta: {stats['weight_change']:+.1f} kg\n")
                f.write(f" BMI Range (Min/Max): {stats['min_bmi']:.2f} / {stats['max_bmi']:.2f}\n")
                f.write(f" Average BMI     : {stats['avg_bmi']:.2f}\n\n")
                f.write("-" * 70 + "\n")
                f.write(" MEASUREMENT HISTORY LOGS:\n")
                f.write("-" * 70 + "\n")
                f.write(f"{'ID':<6} | {'Timestamp':<20} | {'Weight (kg)':<12} | {'Height (m)':<11} | {'BMI':<7} | Category\n")
                f.write("-" * 70 + "\n")
                for r in records:
                    f.write(f"{r['id']:<6} | {r['timestamp']:<20} | {r['weight_kg']:<12.1f} | {r['height_m']:<11.2f} | {r['bmi_value']:<7.2f} | {r['category']}\n")
                f.write("-" * 70 + "\n")
                f.write("\nEnd of Clinical Report.\n")
            return file_path
        except IOError as e:
            raise DatabaseError(f"Failed to write Clinical Report text file: {e}")

    def delete_record(self, record_id: int) -> bool:
        """Delete a record by ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bmi_records WHERE id = ?", (record_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"Error deleting record #{record_id}: {e}")

    def delete_user(self, user_id: int) -> bool:
        """Delete user and all their records."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise DatabaseError(f"Error deleting user #{user_id}: {e}")
