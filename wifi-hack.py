import subprocess
import sys
import time
import os
import json

# Colors for Pro Look
R = "\033[1;31m"  # Red
G = "\033[1;32m"  # Green
Y = "\033[1;33m"  # Yellow
C = "\033[1;36m"  # Cyan
W = "\033[0m"     # Reset

class Main:
    """Scan Wireless devices - Termux Edition (Fixed)"""

    def clear_screen(self):
        os.system('clear')

    def print_banner(self):
        self.clear_screen()
        banner = f"""{G}
    ======================================================
      ____      _                  ____  _     _                 _ 
     / ___|   _| |__   ___ _ __   | __ )(_)___| |__  _ __   ___ (_)
    | |  | | | | '_ \ / _ \ '__|  |  _ \| / __| '_ \| '_ \ / _ \| |
    | |__| |_| | |_) |  __/ |     | |_) | \__ \ | | | | | | (_) | |
     \____\__, |_.__/ \___|_|     |____/|_|___/_| |_|_| |_|\___/|_|
          |___/                                                    
    ======================================================
    {R}         [+] Tool By: Cyber Bishnoi
    {R}         [+] Target: Termux Android
    {W}"""
        print(banner)

    def do_execute(self):
        self.print_banner()
        print(f"{C}[*] Scanning surrounding networks...{W}\n")
        
        # Loading animation
        try:
            for i in range(10):
                sys.stdout.write(f"\r{Y}[*] Searching Airwaves {'.' * (i % 4)}   ")
                sys.stdout.flush()
                time.sleep(0.1)
            print("\r" + " " * 30 + "\r", end="") 
        except KeyboardInterrupt:
            pass

        try:
            result = self.scan()
            
            # Check if result is a valid list of networks
            if result and isinstance(result, list):
                # Table Header
                print(f"{G}{'SSID':<20} {'BSSID':^18} {'FREQ':^6} {'RSSI':^5} {'SEC':^15}{W}")
                print(f"{G}{'-'*70}{W}")
                
                for wifi in result:
                    # Safe extraction of data
                    ssid = wifi.get('ssid', '<Hidden>')[:19]
                    bssid = wifi.get('bssid', 'Unknown')
                    freq = str(wifi.get('frequency_mhz', '0'))
                    rssi = str(wifi.get('rssi', '0'))
                    
                    # Frequency guess for security/band
                    sec = "2.4 GHz"
                    if int(freq) > 4000:
                        sec = "5 GHz"

                    print(f"{Y}{ssid:<20} {bssid:^18} {freq:^6} {rssi:^5} {sec:^15}{W}")
            
            elif result is None:
                # Handled inside scan() already, but just in case
                pass
            else:
                 print(f"\n{R}[!] No networks found.{W}")
                 
        except KeyboardInterrupt:
            print(f"\n{R}[!] Scan stopped.{W}")
        except Exception as e:
            print(f"\n{R}[!] Unexpected Error: {str(e)}{W}")

    def scan(self):
        """Scan using termux-wifi-scaninfo with Error Handling"""
        try:
            cmd = ["termux-wifi-scaninfo"]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = proc.stdout.decode("utf-8")
            
            if not output:
                return None

            try:
                data = json.loads(output)
                
                # FIX: Check if API returned a LIST (Success) or DICT (Error)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    # Agar error message aaya hai to print karo
                    if 'API_ERROR' in data: # Common Termux error key
                        print(f"\n{R}[!] Termux API Error: {data['API_ERROR']}{W}")
                    else:
                        # Print raw dict to see what the error is
                        print(f"\n{R}[!] API Message: {data}{W}")
                    
                    print(f"{Y}Tip: Turn ON Location (GPS) and Grant Permissions.{W}")
                    return None
                    
            except json.JSONDecodeError:
                return None

        except FileNotFoundError:
             print(f"{R}[!] Error: 'termux-api' package not found.{W}")
             print(f"{C}Run: pkg install termux-api{W}")
             return None
            
        return []

if __name__ == "__main__":
    app = Main()
    app.do_execute()