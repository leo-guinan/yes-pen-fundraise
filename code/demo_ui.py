"""
BASE STATION DEMO UI

This is not a dashboard.
This is a contract already alive.

Four zones:
1. THE TRUTH PANEL - Current valuation, time, next price change
2. THE TERMS PANEL - What they get if they press now
3. THE LIVE LEDGER PANEL - History of commitments
4. THE DECISION ZONE - The moment of commitment
"""

import os
import json
import glob
import hashlib
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from trust_v2 import load_round_config, SafeTRoundConfig, current_cap, price_commitment

app = Flask(__name__)
CORS(app)

# Configuration
RAISE_CONFIG_FILE = "SAFE-T_2025_01.json"
LOVE_NOTES_DIR = "love_notes"

# Load genesis raise configuration using TRUST v2
config_path = os.path.join(os.path.dirname(__file__), RAISE_CONFIG_FILE)
try:
    round_config = load_round_config(config_path)
    RAISE_START_DATE = round_config.start_time_utc.replace(tzinfo=None)  # Make naive for display
    FUNDING_ROUND = round_config.round_id
except FileNotFoundError:
    print(f"[!] Warning: {RAISE_CONFIG_FILE} not found, using defaults")
    # Fallback defaults
    RAISE_START_DATE = datetime(2025, 11, 27, 18, 0, 0)
    FUNDING_ROUND = "SAFE-T_2025_01"
    round_config = None
except Exception as e:
    print(f"[!] Error loading config: {e}")
    # Fallback defaults
    RAISE_START_DATE = datetime(2025, 11, 27, 18, 0, 0)
    FUNDING_ROUND = "SAFE-T_2025_01"
    round_config = None

# Next price change interval (in seconds) - price updates every 2 hours
PRICE_UPDATE_INTERVAL = 2 * 60 * 60  # 2 hours


def get_love_notes():
    """Read all LOVE notes from the directory, sorted by timestamp"""
    notes = []
    pattern = os.path.join(LOVE_NOTES_DIR, "love_note_*.json")
    
    for filepath in glob.glob(pattern):
        try:
            with open(filepath, 'r') as f:
                note = json.load(f)
                notes.append(note)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    
    # Sort by timestamp (newest first)
    notes.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
    return notes


def format_time_remaining(seconds):
    """Format seconds as HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_time_since(start_date):
    """Format time since raise started as 'X DAYS · Y HOURS · Z MINUTES'"""
    delta = datetime.now() - start_date
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    return f"{days} DAYS · {hours:02d} HOURS · {minutes:02d} MINUTES"


def get_next_price_change_time():
    """Calculate when the next price change will occur"""
    now = datetime.now()
    seconds_since_start = (now - RAISE_START_DATE).total_seconds()
    intervals_passed = int(seconds_since_start // PRICE_UPDATE_INTERVAL)
    next_interval_start = RAISE_START_DATE + timedelta(seconds=(intervals_passed + 1) * PRICE_UPDATE_INTERVAL)
    seconds_until_next = (next_interval_start - now).total_seconds()
    return max(0, int(seconds_until_next))


@app.route('/')
def index():
    """Serve the main demo UI"""
    return render_template('demo_ui.html')


@app.route('/api/truth')
def api_truth():
    """API endpoint for THE TRUTH PANEL"""
    if round_config:
        # Use timezone-aware datetime for TRUST v2
        now_utc = datetime.now(timezone.utc)
        current_val = current_cap(round_config, now_utc)
    else:
        current_val = 4000000  # Fallback
    
    time_since = format_time_since(RAISE_START_DATE)
    next_change = get_next_price_change_time()
    
    return jsonify({
        "current_valuation": current_val,
        "time_since_opened": time_since,
        "next_price_change_in": format_time_remaining(next_change),
        "next_price_change_seconds": next_change
    })


@app.route('/api/terms')
def api_terms():
    """API endpoint for THE TERMS PANEL"""
    commitment_amount = float(request.args.get('amount', 50000))
    
    if round_config:
        now_utc = datetime.now(timezone.utc)
        snapshot = price_commitment(round_config, commitment_amount, now_utc)
        
        # Format TTL deadline
        ttl_deadline = datetime.fromisoformat(snapshot['ttl_deadline'].replace('Z', '+00:00'))
        ttl_deadline_str = ttl_deadline.strftime("%b %d · %H:%M EST")
        
        # Generate context hash for display
        hash_input = f"{snapshot['timestamp']}{commitment_amount}{snapshot['effective_cap']}"
        context_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
        
        return jsonify({
            "commitment_amount": commitment_amount,
            "funding_round": FUNDING_ROUND,
            "locked_effective_valuation": snapshot['effective_cap'],
            "implied_ownership": snapshot['equity_percentage'] * 100,  # Convert to percentage
            "size_discount": snapshot['size_discount'] * 100,  # Convert to percentage
            "temporal_discount": 0.0,  # TRUST v2 doesn't use temporal discounts
            "ttl_days": round_config.wire_ttl_days,
            "ttl_deadline": ttl_deadline_str,
            "ttl_deadline_iso": snapshot['ttl_deadline'],
            "context_hash": context_hash
        })
    else:
        # Fallback
        return jsonify({
            "commitment_amount": commitment_amount,
            "funding_round": FUNDING_ROUND,
            "locked_effective_valuation": 4000000,
            "implied_ownership": 1.25,
            "size_discount": 0.0,
            "temporal_discount": 0.0,
            "ttl_days": 7,
            "ttl_deadline": "N/A",
            "ttl_deadline_iso": "",
            "context_hash": "00000000"
        })


@app.route('/api/ledger')
def api_ledger():
    """API endpoint for THE LIVE LEDGER PANEL"""
    notes = get_love_notes()
    
    # Format ledger entries
    ledger_entries = []
    for note in notes[:20]:  # Show last 20 entries
        timestamp = note.get('timestamp', 0)
        iso_time = note.get('iso_time', '')
        actor = note.get('actor', 'Unknown')
        
        # Parse ISO time to get HH:MM:SS
        try:
            if iso_time:
                # Handle various ISO formats
                iso_clean = iso_time.replace('Z', '+00:00')
                if '+' not in iso_clean and '-' in iso_clean and iso_clean.count('-') > 2:
                    # Has timezone info
                    dt = datetime.fromisoformat(iso_clean)
                else:
                    # No timezone, assume local
                    dt = datetime.fromisoformat(iso_clean.split('+')[0].split('.')[0])
                time_str = dt.strftime("%H:%M:%S")
            else:
                # Fallback to timestamp
                dt = datetime.fromtimestamp(timestamp)
                time_str = dt.strftime("%H:%M:%S")
        except Exception:
            time_str = "00:00:00"
        
        # Determine status and amount
        note_type = note.get('type', 'love_note')
        context = note.get('context', {})
        
        if note_type == 'investment_commitment':
            # Extract from context block (new structure) or top-level (legacy)
            amount = context.get('commitment_amount', note.get('amount', 0))
            raw_status = context.get('status', note.get('status', 'awaiting_wire'))
            
            # Format status for display
            if raw_status == 'awaiting_wire':
                status = 'LOCKED · Awaiting wire'
            elif raw_status == 'confirmed':
                status = 'CONFIRMED'
            elif raw_status == 'expired':
                status = 'EXPIRED'
            else:
                status = raw_status.upper()
            
            ledger_entries.append({
                "time": time_str,
                "actor": actor,
                "amount": f"${amount:,.0f}",
                "status": status
            })
        elif note_type == 'love_note':
            # Generic YES signal
            ledger_entries.append({
                "time": time_str,
                "actor": actor,
                "amount": "—",
                "status": "YES"
            })
    
    return jsonify({
        "entries": ledger_entries
    })


@app.route('/api/commit', methods=['POST'])
def api_commit():
    """Handle YesPen commitment"""
    data = request.json
    commitment_amount = float(data.get('amount', 50000))
    
    if not round_config:
        return jsonify({"success": False, "error": "Round configuration not loaded"}), 500
    
    # Compute terms via TRUST v2
    now_utc = datetime.now(timezone.utc)
    snapshot = price_commitment(round_config, commitment_amount, now_utc)
    
    # Generate context hash
    hash_input = f"{snapshot['timestamp']}{commitment_amount}{snapshot['effective_cap']}"
    context_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
    
    # Parse timestamp for LOVE note
    commit_timestamp = datetime.fromisoformat(snapshot['timestamp'].replace('Z', '+00:00'))
    timestamp_int = int(commit_timestamp.timestamp())
    
    # Create LOVE note with full pricing snapshot in context
    love_note = {
        "type": "investment_commitment",
        "actor": f"YesPen_{len(get_love_notes()) + 1:03d}",
        "timestamp": timestamp_int,
        "iso_time": snapshot['timestamp'],
        "action": "COMMITMENT",
        "context": {
            "round_id": snapshot['round_id'],
            "role": "investor_commitment",
            "commitment_amount": snapshot['commitment_amount'],
            "base_valuation": snapshot['base_cap'],
            "size_discount": snapshot['size_discount'],
            "effective_valuation": snapshot['effective_cap'],
            "equity_percentage": snapshot['equity_percentage'],
            "ttl_deadline": snapshot['ttl_deadline'],
            "status": "awaiting_wire"
        },
        "machine_signature": "pending_crypto_layer"
    }
    
    # Save LOVE note
    os.makedirs(LOVE_NOTES_DIR, exist_ok=True)
    filename = f"love_note_{love_note['timestamp']}.json"
    filepath = os.path.join(LOVE_NOTES_DIR, filename)
    
    with open(filepath, 'w') as f:
        json.dump(love_note, f, indent=2)
    
    # Format response
    ttl_deadline = datetime.fromisoformat(snapshot['ttl_deadline'].replace('Z', '+00:00'))
    ttl_deadline_str = ttl_deadline.strftime("%b %d · %H:%M EST")
    
    return jsonify({
        "success": True,
        "commitment": {
            "investment": commitment_amount,
            "valuation": snapshot['effective_cap'],
            "ownership": snapshot['equity_percentage'] * 100,  # Convert to percentage
            "ttl_deadline": ttl_deadline_str
        },
        "love_note": love_note,
        "context_hash": context_hash
    })


if __name__ == '__main__':
    print("=" * 60)
    print(" BASE STATION DEMO UI")
    print(" This is not a dashboard.")
    print(" This is a contract already alive.")
    print("=" * 60)
    print(f"\nServing at http://localhost:5005")
    
    if round_config:
        print(f"\n📄 Loaded genesis raise: {round_config.round_id}")
        print(f"   Pricing Engine: TRUST v1.0")
        print(f"   Initial Cap: ${round_config.initial_cap:,.0f}")
        print(f"   Daily Decay: {round_config.daily_decay_rate * 100:.2f}%")
        print(f"   Minimum Floor: ${round_config.floor_cap:,.0f}")
        print(f"   TTL Days: {round_config.wire_ttl_days}")
        
        # Show current valuation
        now_utc = datetime.now(timezone.utc)
        current_val = current_cap(round_config, now_utc)
        print(f"\nRaise started: {RAISE_START_DATE}")
        print(f"Current valuation: ${current_val:,.0f}")
    else:
        print(f"\n[!] Using fallback configuration")
        print(f"Raise started: {RAISE_START_DATE}")
    
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5005)

