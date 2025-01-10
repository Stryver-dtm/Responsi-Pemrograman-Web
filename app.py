from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': "ndpeu.h.filess.io",
    'database': "dbkuliah_facingwin",
    'user': "dbkuliah_facingwin",
    'password': "902b51f2966a15f92bce5b751e3aa111b3c1da96",
    'port': 3305
}

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MariaDB: {e}")
        return None

# Example route to test database connection
@app.route('/db-info', methods=['GET'])
def db_info():
    connection = get_db_connection()
    if connection:
        try:
            db_info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            current_db = cursor.fetchone()
            cursor.close()
            connection.close()
            return jsonify({
                "message": "Connected to MariaDB",
                "server_version": db_info,
                "current_database": current_db[0] if current_db else None
            })
        except Error as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
