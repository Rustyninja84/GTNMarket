# Star Forge GTN Windows capture prototype

This prototype uses **screen capture and local OCR only**. It does not read SWTOR memory, intercept traffic, control gameplay, or send data to GitHub. It cannot claim a server-wide live GTN feed. Check EA/SWTOR third-party software rules before use.

## Windows setup
1. Install Python 3.11+ from python.org (check Add Python to PATH).
2. Install **Tesseract OCR for Windows** and add its installation directory to PATH.
3. In PowerShell in this folder run: `py -m pip install -r requirements.txt`
4. Run: `py companion.py`
5. Launch SWTOR in Fullscreen (Windowed), open the GTN listings, and enter a rectangle covering the listing rows (Left, Top, Width, Height).
6. Click **Capture once**. Adjust rectangle until the recognized text matches the visible listings. Optionally click **Start every 15 seconds**.
7. The raw unverified observations are saved at `Documents/GTNMarket/ocr_observations.jsonl` and never uploaded.

## Next milestone
Provide one real GTN screenshot to tune row detection and validate item name, quantity, unit price and observation time. After validation, implement a consent-based authenticated upload endpoint; do **not** embed a GitHub token in a public website or source repository. The current GitHub Pages site cannot securely receive direct anonymous writes.

No market-wide live feed exists in this prototype; only on-screen listings can be observed.
