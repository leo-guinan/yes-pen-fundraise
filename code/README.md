# YesPen Base Station

## Demo UI

The BASE STATION DEMO UI is not a dashboard. It is a contract already alive.

### Running the Demo

```bash
# Install dependencies
uv sync

# Run the demo UI
python demo_ui.py
```

Then open http://localhost:5000 in your browser.

### What You'll See

**Four Zones:**

1. **THE TRUTH PANEL** (Top third)
   - Current effective valuation
   - Time since raise opened
   - Next price change countdown

2. **THE TERMS PANEL** (Left middle)
   - Commitment amount input
   - Locked effective valuation
   - Implied ownership
   - Discounts applied
   - TTL window and deadline

3. **THE LIVE LEDGER PANEL** (Right middle)
   - Scrollable history of all commitments
   - Timestamps, actors, amounts, status

4. **THE DECISION ZONE** (Bottom third)
   - Current context hash
   - Terms snapshot
   - "PRESS YES TO LOCK TERMS" button
   - After press: Commitment recorded + LOVE note displayed

### YesPen Integration

To connect a physical YesPen device:

```bash
# Set commitment amount (optional, defaults to $50,000)
export DEMO_COMMITMENT_AMOUNT=100000

# Run base station (connects to YesPen via BLE)
python station.py
```

When the YesPen button is pressed, it will automatically trigger a commit in the demo UI (if running).

### Configuration

Edit `demo_ui.py` to adjust:
- `RAISE_START_DATE` - When the raise started
- `FUNDING_ROUND` - Round identifier
- TRUST engine parameters (in `trust.py`)

### Design Philosophy

This UI is designed to feel:
- **Adult** - No animations, no fluff
- **Cold** - Just facts, no narrative
- **Final** - This is law, not persuasion
- **Dignified** - Silence + consequence
- **Inevitable** - The machine is already running

It does NOT show:
- Dashboards
- Code
- Config files
- Crypto anything
- Animations
- Stories
- Opinions

The power is silence + consequence.

