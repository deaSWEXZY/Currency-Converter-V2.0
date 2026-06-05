# 💱 Currency Converter GUI (with Advanced Arduino Display [LINUX ONLY])

A sleek, dark-mode desktop application built with Python and Tkinter that fetches real-time, global exchange rates. It features a complete conversion engine and an advanced Linux-only physical hardware integration to display live conversions on an external LCD screen.

---

## ✨ Core Features
* **Global Currency Support:** Dynamically fetches up-to-date international rates using the Open Exchange Rates API.
* **Modern UI:** Clean, custom dark-mode interface utilizing styled Tkinter elements.
* **Robust Input Validation:** Built-in exception handling to prevent crashes from invalid numbers or empty fields.
* **Advanced Hardware Mirror (Linux Only):** Automatically streams your active conversions over Serial (/dev/ttyUSB0) to a physical 16x2 LCD screen.

---

## 💻 Software Setup (Python)

**1. Clone the repository and navigate inside:**
git clone https://github.com/swezxyCode/Currency-Converter-Advanced.git
cd Currency-Converter-Advanced

**2. Create a virtual environment and install requirements:**
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirments.txt

*(Note: If your Linux system lacks the core Tkinter packages, install them via: sudo apt install python3-tk)*

**3. Launch the Application:**
python main.py

*The GUI app runs independently. If no hardware is plugged in, it automatically skips the serial update so you can use the desktop converter normally without crashing.*

---

## 🔌 Advanced Mode: Linux Hardware Integration

If you want to use the desktop layout alongside a physical display tracker, follow these steps on Ubuntu/Linux:

### 1. Hardware Connections
* Connect a 16x2 LCD with an I2C module to your Arduino board.
* **Wiring:** * VCC -> 5V
  * GND -> GND
  * SDA -> A4
  * SCL -> A5
* Open sketch_connecting.ino in the Arduino IDE, install the LiquidCrystal_I2C library, and flash your board.

### 2. Grant Serial Port Permissions
Linux locks down raw USB communication by default. Run this command so your Python environment can stream data to the USB port without requiring sudo:

sudo usermod -a -G dialout $USER

*(Important: You must log out of your Ubuntu user account and log back in for this permission change to take effect!)*

---

## ⚙️ How the Engine Syncs
* **The Software:** When you select your currencies and click Convert, the application processes the API math locally, updates the Tkinter UI label, and pushes a parsed byte string structure (Amount From -> To|Result) down the USB line.
* **The Hardware:** The Arduino continuously listens to the stream, waits for the structural line-break (\n), strips the formatting boundary (|), and maps the data perfectly onto your desk display with built-in truncation safety steps to prevent character glitching.
