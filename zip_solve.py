import zipfile
import os
import time

# ==========================================
# ⚙️ SETTING: WHICH FILE ARE WE TESTING?
# ==========================================
# Change this to bravo_layer_50.zip or charlie_layer_50.zip to test the others
STARTING_ZIP = "alpha_layer_50.zip" 
# ==========================================

print(f"[*] INITIATING DECRYPTION SEQUENCE ON {STARTING_ZIP}...\n")

current_target = STARTING_ZIP

# Loop safely up to 100 times (just in case) to dig through the layers
for _ in range(100):
    
    # Open the current zip file
    with zipfile.ZipFile(current_target, 'r') as zf:
        # Look at everything inside the zip
        contents = zf.namelist()
        
        # Find the "needle" (ignore all the fake server_log text files)
        next_file = None
        for item in contents:
            if item.endswith(".zip") or item == "clue.txt":
                next_file = item
                break
                
        if not next_file:
            print("[-] ERROR: Dead end reached. No valid file found.")
            break
            
        # Extract ONLY the next zip file or the final clue
        zf.extract(next_file)
        
    # Delete the outer shell we just broke open (but don't delete the original starting file)
    if current_target != STARTING_ZIP:
        os.remove(current_target)
        
    current_target = next_file
    
    # Did we hit the core?
    if current_target == "clue.txt":
        print("[+] CORE ACCESSED. DECRYPTING INTEL:\n")
        print("="*50)
        
        with open("clue.txt", "r") as f:
            print(f.read())
            
        print("="*50)
        print("\n[*] Cleanup complete. Operation successful.")
        break