import asyncio
from bleak import BleakScanner

async def main():
    print("🕵️  Scanning airwaves for 5 seconds...")
    
    # Scan for devices
    devices = await BleakScanner.discover(timeout=5.0)
    
    found_pen = False
    
    print("\n--- DEVICES FOUND ---")
    for d in devices:
        # Print everything to see what's out there
        name = d.name or "Unknown"
        print(f"Name: {name:20} | ID: {d.address}")
        
        if "YesPe" in name:
            found_pen = True

    print("-" * 30)
    
    if found_pen:
        print("✅ SUCCESS: 'YesPen' was found! Update your station.py logic.")
    else:
        print("❌ FAILURE: 'YesPen' not seen.")
        print("   1. Is the battery connected?")
        print("   2. Is a phone currently connected? (Disconnect it!)")
        print("   3. Try pressing the Reset button on the Xiao.")

if __name__ == "__main__":
    asyncio.run(main())
