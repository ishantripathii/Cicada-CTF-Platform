import os
import zipfile
import random

print("Building the Nested Haystacks for Alpha, Bravo, and Charlie...")

# ==========================================
# ⚙️ GAME MASTER SETTINGS ⚙️
# ==========================================
NUM_LAYERS = 50

TEAMS = {
    "ALPHA": {"network": "CODEX_NODE_ALPHA", "ip": "192.168.137.1"},
    "BRAVO": {"network": "CODEX_NODE_BRAVO", "ip": "192.168.137.1"},
    "CHARLIE": {"network": "CODEX_NODE_CHARLIE", "ip": "192.168.137.1"}
}
# ==========================================

for team, data in TEAMS.items():
    print(f"\n[*] Generating payload for {team}...")
    
    # 1. Customize the riddle for this specific team's path
    REAL_CLUE = f"""TARGET NETWORK: {data['network']}
		    Password:codex123
The IP of the host is: {data['ip']}.

All ships sail from a port, you have to find the specific one to make your ship sail.
Navigate the coastal waters from bearing 2000 to 2100.
Sailors should use a map while sailing.
Proceed to AB4 Gate 1 Entrance."""

    previous_zip = None

    # We build from the inside (Level 1) to the outside (Level 50)
    for level in range(1, NUM_LAYERS + 1):
        current_zip_name = f"layer_{level}.zip"
        
        with zipfile.ZipFile(current_zip_name, 'w') as zf:
            # 1. Add the core payload
            if level == 1:
                # The very center gets the real clue
                with open("clue.txt", "w") as f:
                    f.write(REAL_CLUE)
                zf.write("clue.txt")
                os.remove("clue.txt")
            else:
                # Every other level swallows the previous zip file
                zf.write(previous_zip)
                os.remove(previous_zip) # Clean up the old one
                
            # 2. Add the "Hay" (15 decoy text files per level)
            for d in range(1, 16):
                fake_name = f"server_log_{level}_{d}.txt"
                with open(fake_name, "w") as f:
                    f.write(f"ERROR: Node {random.randint(100,999)} is unreachable.")
                zf.write(fake_name)
                os.remove(fake_name)
                
        previous_zip = current_zip_name

    # Rename the final layer_50.zip to the team's specific name
    final_name = f"{team.lower()}_layer_{NUM_LAYERS}.zip"
    if os.path.exists(final_name):
        os.remove(final_name)
    os.rename(previous_zip, final_name)
    
    print(f"[+] Done! Give the {team} players the file named: {final_name}")

print("\n[*] ALL THREE PACKAGES READY FOR DEPLOYMENT.")