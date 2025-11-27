import asyncio
import json
import time
import os
from datetime import datetime, timezone
from bleak import BleakScanner, BleakClient

# Optional: Demo UI integration (only import if available)
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False

# TRUST v2 integration
try:
    from trust_v2 import load_round_config, price_commitment
    TRUST_V2_AVAILABLE = True
except ImportError:
    TRUST_V2_AVAILABLE = False
    print("[!] Warning: TRUST v2 not available, using basic LOVE notes")

# ========================================================
# CONFIGURATION - UPDATE THESE TO MATCH YOUR FIRMWARE
# ========================================================
DEVICE_NAME = "YesPen"
# Replace these with the UUIDs from your Arduino Sketch
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0" 
CHAR_DECISION_UUID = "12345678-1234-5678-1234-56789abcdef3" 
CHAR_CONTEXT_UUID = "12345678-1234-5678-1234-56789abcdef2"
CHAR_PEN_ID_UUID = "12345678-1234-5678-1234-56789abcdef1"

# FIRMWARE REQUIREMENT (Poll-Friendly Semantics):
# On button press, firmware should:
#   decisionChar.write8(1);
#   yesFlash();
#   // DO NOT immediately write back to 0
# The base station will reset it to 0 after processing the LOVE Note
# The context we are "loading" into the moment
CURRENT_CONTEXT = {
    "session_id": "demo_workshop_01",
    "role": "investor_agreement",
    "terms_hash": "sha256_of_term_sheet_v1"
}

# Optional: Demo UI integration
# If DEMO_UI_URL is set, YesPen presses will trigger commits in the demo UI
DEMO_UI_URL = os.getenv("DEMO_UI_URL", "http://localhost:5005")
DEMO_COMMITMENT_AMOUNT = float(os.getenv("DEMO_COMMITMENT_AMOUNT", "50000"))

# Load TRUST v2 round configuration
ROUND_CONFIG = None
if TRUST_V2_AVAILABLE:
    config_path = os.path.join(os.path.dirname(__file__), "SAFE-T_2025_01.json")
    try:
        ROUND_CONFIG = load_round_config(config_path)
        print(f"[+] Loaded TRUST v2 config: {ROUND_CONFIG.round_id}")
    except FileNotFoundError:
        print(f"[!] Warning: SAFE-T_2025_01.json not found")
    except Exception as e:
        print(f"[!] Error loading TRUST config: {e}")

# ========================================================

def save_love_note(note_data):
    """Writes the LOVE Note to a JSON file (The Artifact)"""
    filename = f"love_note_{note_data['timestamp']}.json"
    
    # Ensure directory exists
    os.makedirs("love_notes", exist_ok=True)
    filepath = os.path.join("love_notes", filename)
    
    with open(filepath, 'w') as f:
        json.dump(note_data, f, indent=2)
    
    print(f"\n[✨] LOVE Note Minted: {filepath}")
    print(json.dumps(note_data, indent=2))
    print("\nWaiting for next event...")

async def process_yes_signal(client):
    """Processes a YES signal and resets the characteristic"""
    print("\n[!] YES SIGNAL RECEIVED")
    
    # Capture exact timestamp of YesPen press
    press_timestamp_utc = datetime.now(timezone.utc)
    timestamp_int = int(press_timestamp_utc.timestamp())
    
    # If TRUST v2 is available and config loaded, compute pricing snapshot
    context_data = CURRENT_CONTEXT.copy()  # Start with base context
    
    if ROUND_CONFIG and TRUST_V2_AVAILABLE:
        # Compute pricing at exact moment of press
        snapshot = price_commitment(ROUND_CONFIG, DEMO_COMMITMENT_AMOUNT, press_timestamp_utc)
        
        # Inject full pricing snapshot into context
        context_data = {
            "round_id": snapshot['round_id'],
            "role": "investor_commitment",
            "commitment_amount": snapshot['commitment_amount'],
            "base_valuation": snapshot['base_cap'],
            "size_discount": snapshot['size_discount'],
            "effective_valuation": snapshot['effective_cap'],
            "equity_percentage": snapshot['equity_percentage'],
            "ttl_deadline": snapshot['ttl_deadline'],
            "status": "awaiting_wire"
        }
        
        print(f"[+] Pricing computed: ${snapshot['effective_cap']:,.0f} cap, {snapshot['equity_percentage']*100:.2f}% equity")
    
    # Construct the LOVE Note
    love_note = {
        "type": "investment_commitment" if ROUND_CONFIG else "love_note",
        "timestamp": timestamp_int,
        "iso_time": press_timestamp_utc.isoformat(),
        "actor": "YesPen_001", # In future, read this from PEN_ID char
        "action": "COMMITMENT" if ROUND_CONFIG else "YES",
        "context": context_data,
        "machine_signature": "pending_crypto_layer"
    }
    
    save_love_note(love_note)
    
    # Optional: Trigger commit in demo UI if running
    if HAS_AIOHTTP:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{DEMO_UI_URL}/api/commit",
                    json={"amount": DEMO_COMMITMENT_AMOUNT},
                    timeout=aiohttp.ClientTimeout(total=2)
                ) as response:
                    if response.status == 200:
                        print(f"[+] Demo UI commit triggered: ${DEMO_COMMITMENT_AMOUNT:,.0f}")
                    else:
                        print(f"[!] Demo UI not responding (status {response.status})")
        except Exception as e:
            # Demo UI not running or not accessible - that's okay
            print(f"[!] Demo UI integration skipped: {e}")
    
    # Reset the characteristic to 0 after processing
    # This allows polling to work and ensures we've processed the event
    try:
        await client.write_gatt_char(CHAR_DECISION_UUID, b'\x00')
        print("[+] Decision characteristic reset to 0")
    except Exception as e:
        print(f"[!] Warning: Could not reset decision characteristic: {e}")

def create_notification_handler(client):
    """Creates a notification handler that has access to the client"""
    async def notification_handler(sender, data):
        """Triggered when the Yes Pen sends a notification"""
        print(f"\n[DEBUG] Notification received from {sender}")
        print(f"[DEBUG] Raw data: {data.hex()} (length: {len(data)})")
        
        try:
            if len(data) > 0:
                val = int.from_bytes(data, byteorder='little')
                print(f"[DEBUG] Parsed value: {val}")
                
                if val == 1:
                    await process_yes_signal(client)
                else:
                    print(f"[DEBUG] Received value {val}, not YES (expected 1)")
            else:
                print("[DEBUG] Empty notification received")
        except Exception as e:
            print(f"[!] Error processing notification: {e}")
            print(f"[DEBUG] Raw bytes: {data}")
    
    return notification_handler

async def main():
    print(f"[-] Scanning for {DEVICE_NAME}...")
    devices = await BleakScanner.discover(timeout=5.0)
    
    device = None
    for d in devices:
        print(d.name, d.address)
        if d.name == DEVICE_NAME:
            print(f"[+] Found {DEVICE_NAME} ({d.address})")
            device = d
            break
    
    if not device:
        print(f"[x] Could not find {DEVICE_NAME}. Is it powered on?")
        return
    
    print("[-] Connecting...")
    async with BleakClient(device) as client:
        print(f"[+] Connected to {DEVICE_NAME}.")
        
        # === THE FIX IS HERE ===
        print("[-] Waiting for services to stabilize...")
        await asyncio.sleep(2.0) # Give the Mac time to read the map
        
        # Discover and print all services/characteristics for debugging
        print("[-] Discovering services and characteristics...")
        try:
            services = client.services
            service_list = list(services)
            print(f"[+] Found {len(service_list)} service(s):")
            decision_char_found = False
            for service in service_list:
                print(f"  Service: {service.uuid}")
                for char in service.characteristics:
                    props = []
                    if "read" in char.properties:
                        props.append("READ")
                    if "write" in char.properties:
                        props.append("WRITE")
                    if "notify" in char.properties:
                        props.append("NOTIFY")
                    if "indicate" in char.properties:
                        props.append("INDICATE")
                    print(f"    Characteristic: {char.uuid} [{', '.join(props)}]")
                    if char.uuid == CHAR_DECISION_UUID:
                        decision_char_found = True
                        if "notify" not in char.properties:
                            print(f"[!] WARNING: Decision characteristic exists but does NOT support NOTIFY!")
                            print(f"[!] It supports: {char.properties}")
            if not decision_char_found:
                print(f"[!] WARNING: Decision characteristic {CHAR_DECISION_UUID} not found!")
        except Exception as e:
            print(f"[!] Error discovering services: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"[+] Ready to interact.")
        # =======================
        # 1. Write Context (Simulating setting the stage)
        # We convert the context ID/Hash to bytes
        context_bytes = CURRENT_CONTEXT["session_id"].encode('utf-8')
        try:
            await client.write_gatt_char(CHAR_CONTEXT_UUID, context_bytes)
            print(f"[+] Context '{CURRENT_CONTEXT['session_id']}' sent to Pen.")
        except Exception as e:
            print(f"[!] Warning: Could not write context (Feature might not be in FW yet): {e}")

        # 2. Subscribe to Decisions
        # Create notification handler with access to client for reset functionality
        notification_handler = create_notification_handler(client)
        
        print("[-] Subscribing to Decision Stream...")
        try:
            await client.start_notify(CHAR_DECISION_UUID, notification_handler)
            print(f"[+] Successfully subscribed to {CHAR_DECISION_UUID}")
            print("[+] Notification handler active - waiting for button press...")
            print("[+] After processing YES, characteristic will be reset to 0")
        except Exception as e:
            print(f"[!] ERROR: Failed to subscribe to notifications: {e}")
            print(f"[!] Check that UUID {CHAR_DECISION_UUID} exists and supports NOTIFY")
            print("[!] Continuing anyway, but notifications may not work...")

        print("\n" + "="*40)
        print(" BASE STATION ACTIVE - WAITING FOR 'YES'")
        print(" Press Ctrl+C to stop")
        print("="*40 + "\n")

        # Also poll the characteristic periodically as a fallback
        # Some devices don't send notifications reliably
        last_value = None
        poll_count = 0
        
        # Keep the script running forever (until Ctrl+C)
        try:
            while True:
                await asyncio.sleep(1)
                poll_count += 1
                
                # Every 2 seconds, try reading the characteristic value
                # This helps debug if notifications aren't working
                # With poll-friendly firmware, value stays 1 until we reset it
                if poll_count % 2 == 0:
                    try:
                        value = await client.read_gatt_char(CHAR_DECISION_UUID)
                        current_val = int.from_bytes(value, byteorder='little') if len(value) > 0 else 0
                        if current_val != last_value:
                            print(f"[DEBUG] Polled value changed: {last_value} -> {current_val}")
                            if current_val == 1:
                                # Process YES signal (this will also reset to 0)
                                await process_yes_signal(client)
                            last_value = current_val
                    except Exception as e:
                        # Characteristic might not support read, that's okay
                        pass
        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            pass
            
        print("[-] Disconnecting...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[x] Session ended.")
