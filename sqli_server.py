import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- 1. SETUP THE DATABASE ---
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    
    # Table 1: The Public Directory (Columns: alias, specialty)
    cursor.execute('''CREATE TABLE agents (alias TEXT, specialty TEXT)''')
    cursor.execute("INSERT INTO agents VALUES ('Cipher', 'Network Exploitation')")
    cursor.execute("INSERT INTO agents VALUES ('Ghost', 'Social Engineering')")
    cursor.execute("INSERT INTO agents VALUES ('Zero', 'Cryptography')")
    
    # Table 2: The Hidden Target (Columns: secret_name, data)
    cursor.execute('''CREATE TABLE classified_intel (secret_name TEXT, data TEXT)''')
    cursor.execute("INSERT INTO classified_intel VALUES ('NEXT_STATION', 'LOCATION: [INSERT STATION 3 LOCATION]. GO NOW.')")
    
    conn.commit()
    return conn

db_conn = init_db()
