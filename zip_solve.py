import zipfile
import os
import time

STARTING_ZIP = "alpha_layer_50.zip" 

print(f"[*] INITIATING DECRYPTION SEQUENCE ON {STARTING_ZIP}...\n")

current_target = STARTING_ZIP

for _ in range(100):
    
    with zipfile.ZipFile(current_target, 'r') as zf:
        contents = zf.namelist()
        
        next_file = None
        for item in contents:
            if item.endswith(".zip") or item == "clue.txt":
                next_file = item
                break
                
        if not next_file:
            print("[-] ERROR: Dead end reached. No valid file found.")
            break
            
        zf.extract(next_file)
        
    if current_target != STARTING_ZIP:
        os.remove(current_target)
        
    current_target = next_file
    
    if current_target == "clue.txt":
        print("[+] CORE ACCESSED. DECRYPTING INTEL:\n")
        print("="*50)
        
        with open("clue.txt", "r") as f:
            print(f.read())
            
        print("="*50)
        print("\n[*] Cleanup complete. Operation successful.")
        break
