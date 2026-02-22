from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# ==========================================
# ⚙️ GAME MASTER SETTINGS (CHANGE THESE!) ⚙️
# ==========================================

# Choose which team this laptop is hosting: "ALPHA", "BRAVO", or "CHARLIE"
NODE_TEAM = "ALPHA" 

# Put this laptop's actual Hotspot IP here
NODE_IP = "192.168.137.1" 

# Put the 3 distinct passwords you get from the next station handlers here:
STATION_PASSWORDS = {
    "ALPHA": "NexusOrbit84",
    "BRAVO": "UrbanVortex95",
    "CHARLIE": "GraniteVault83"
}

# ==========================================

DB_FILE = f'database_{NODE_TEAM.lower()}.db'

# --- 1. DATABASE SETUP ---
def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Public Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sectors (sector_name TEXT, status TEXT)''')
    cursor.execute("DELETE FROM sectors")
    cursor.execute("INSERT INTO sectors VALUES ('PUBLIC-TERMINAL', 'ONLINE - RESTRICTED MODE')")
    cursor.execute("INSERT INTO sectors VALUES ('TACTICAL-MAP', 'ERROR: DATA CORRUPTED. CHECK INTEL_TABLES.')")

    # 2. Team-Specific Secret Tables 
    cursor.execute("DROP TABLE IF EXISTS intel_alpha")
    cursor.execute("DROP TABLE IF EXISTS intel_bravo")
    cursor.execute("DROP TABLE IF EXISTS intel_charlie")

    # Automatically grab the correct password for this specific laptop!
    current_password = STATION_PASSWORDS[NODE_TEAM]
    formatted_password = f"ACCESS CODE FOR NEXT STATION: {current_password}"

    if NODE_TEAM == "ALPHA":
        cursor.execute('''CREATE TABLE intel_alpha (riddle_clue TEXT, password TEXT)''')
        riddle = """Where echoes of victory circle in four directions,\nI rest in the silence between rival affections.\nNot a field, yet I see every battle begin,\nA thin breath of space where no game can win."""
        cursor.execute("INSERT INTO intel_alpha VALUES (?, ?)", (riddle, formatted_password))
        
    elif NODE_TEAM == "BRAVO":
        cursor.execute('''CREATE TABLE intel_bravo (riddle_clue TEXT, password TEXT)''')
        riddle = """The painter dreams, the lawyer defends,\nThrough corridors where knowledge bends,\nFind the pause where both worlds meet,\nPass not beyond till this place you greet."""
        cursor.execute("INSERT INTO intel_bravo VALUES (?, ?)", (riddle, formatted_password))
        
    elif NODE_TEAM == "CHARLIE":
        cursor.execute('''CREATE TABLE intel_charlie (riddle_clue TEXT, password TEXT)''')
        riddle = """A fruit from a grander, older tree,\nBeside new books yet to be free,\nBehind the blue wings, away from the crowd,\nRests the child of a touch who is proud"""
        cursor.execute("INSERT INTO intel_charlie VALUES (?, ?)", (riddle, formatted_password))

    conn.commit()
    conn.close()
    print(f"[*] Database Initialized for {NODE_TEAM} Team.")
    print(f"[*] Hosted at: {NODE_IP}:2026")
# --- 2. MATRIX RAIN UI DESIGN ---
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CODEX | CLASSIFIED INTEL</title>
    <style>
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
        
        body { 
            background-color: #000000; 
            color: #c9d1d9; 
            font-family: 'Segoe UI', 'Courier New', monospace; 
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            overflow: hidden;
        }

        #matrixCanvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        body::before {
            content: " ";
            display: block;
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 2;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }

        .container { 
            position: relative;
            width: 650px;
            background: rgba(13, 17, 23, 0.95);
            border-radius: 12px;
            padding: 50px;
            z-index: 3;
            text-align: center;
            border: 2px solid #39ff14; 
            box-shadow: 0 0 30px rgba(57, 255, 20, 0.3), inset 0 0 10px rgba(57, 255, 20, 0.1);
            backdrop-filter: blur(5px);
        }

        .header {
            border-bottom: 2px solid #ff7b72; 
            margin-bottom: 30px;
            padding-bottom: 15px;
        }

        h2 { 
            color: #ff7b72; 
            text-transform: uppercase; 
            letter-spacing: 3px; 
            margin: 0;
            font-size: 1.5em;
            text-shadow: 0 0 10px rgba(255, 123, 114, 0.4);
        }

        .hack-alert { 
            color: #ff7b72; 
            font-weight: bold; 
            animation: blink 0.8s infinite; 
            margin-bottom: 20px; 
            font-family: monospace;
            border: 1px solid #ff7b72;
            padding: 10px;
            background: rgba(255, 123, 114, 0.1);
        }

        .input-group { margin: 30px 0; display: flex; justify-content: center; }

        input { 
            background: #0d1117; 
            border: 1px solid #39ff14; 
            color: #aff5b4; 
            padding: 12px 15px; 
            width: 60%; 
            border-radius: 6px 0 0 6px;
            outline: none;
            font-family: monospace;
            font-size: 1em;
            transition: all 0.3s;
        }

        input:focus { box-shadow: 0 0 15px rgba(57, 255, 20, 0.5); }

        button { 
            background: #238636; 
            color: #ffffff; 
            border: none; 
            padding: 12px 25px; 
            cursor: pointer; 
            font-weight: bold; 
            border-radius: 0 6px 6px 0;
            transition: background 0.3s;
            font-size: 1em;
        }

        button:hover { background: #2ea043; }

        .result-box { 
            margin-top: 30px; 
            text-align: left; 
            background: #0d1117;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #ff7b72; 
        }

        .riddle-output { 
            white-space: pre-wrap; 
            color: #aff5b4; 
            font-family: 'Courier New', monospace;
            line-height: 1.6;
            font-size: 1.1em;
        }

        .error-log { color: #ff7b72; font-family: monospace; font-size: 0.9em; }

        .footer {
            margin-top: 40px;
            font-size: 0.7em;
            color: #39ff14; 
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <canvas id="matrixCanvas"></canvas>

    <div class="container">
        
        {% if show_hack %}
            <div class="hack-alert">>> CRITICAL VULNERABILITY DETECTED: SQL INJECTION POSSIBLE</div>
        {% endif %}

        <div class="header">
            <h2>[ NODE {{ node }} : TOP SECRET GEOLOCATION DATABASE ]</h2>
        </div>
        
        <p style="color: #8b949e; font-size: 0.9em;">ENTER SECTOR ID TO RETRIEVE COORDINATES</p>
        
        <form method="POST" class="input-group">
            <input type="text" name="search" placeholder="e.g. PUBLIC-TERMINAL" autocomplete="off" autofocus>
            <button type="submit">SCAN</button>
        </form>

        {% if results is not none %}
            <div class="result-box">
                {% if error_msg %}
                    <p class="error-log">SYSTEM FAILURE: SQL SYNTAX ERROR DETECTED</p>
                    <p style="color: #484f58; font-size: 0.8em;">DEBUG LOG: {{ error_msg }}</p>
                {% elif results|length == 0 %}
                    <p style="color: #ff7b72;">NO SECTOR FOUND. ACCESS DENIED.</p>
                {% else %}
                    {% for row in results %}
                        <div class="riddle-output">{{ row[0] }}</div>
                        {% if row[1] %}<p style="color: #58a6ff; margin-top: 10px; font-size: 0.8em;">STATUS: {{ row[1] }}</p>{% endif %}
                        <hr style="border: 0; border-top: 1px solid #30363d; margin: 15px 0;">
                    {% endfor %}
                {% endif %}
            </div>
        {% endif %}
        
        <div class="footer">
            SECURE CONNECTION // NODE: {{ ip }} // CODEX TERMINAL v4
        </div>
    </div>

    <script>
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        const chars = '010101010123456789';
        const charArray = chars.split('');
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = [];
        for (let x = 0; x < columns; x++) { drops[x] = 1; }

        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = charArray[Math.floor(Math.random() * charArray.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) { drops[i] = 0; }
                drops[i]++;
            }
        }
        setInterval(draw, 33);
    </script>
</body>
</html>
'''

# --- 3. SERVER LOGIC ---
@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    error_msg = None
    show_hack = False
    
    if request.method == 'POST':
        search_term = request.form.get('search', '')
        
        # Trigger the red alert if they use a single quote
        if "'" in search_term:
            show_hack = True
            
        # The Vulnerable Query
        query = f"SELECT sector_name, status FROM sectors WHERE sector_name = '{search_term}'"
        
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
        except Exception as e:
            error_msg = str(e)
            results = []
            
    return render_template_string(HTML_PAGE, results=results, error_msg=error_msg, show_hack=show_hack, node=NODE_TEAM, ip=NODE_IP)

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=2026)