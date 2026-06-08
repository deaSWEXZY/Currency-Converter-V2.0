# Currency Converter GUI with Arduino LCD Display

A dark-mode desktop application built with Python and Tkinter that fetches real-time exchange rates. It features a complete conversion engine paired with a hardware integration layer that automatically detects your connected Arduino board to display live conversions on an external LCD screen across Windows, macOS, and Linux.

---

## Core Features

* **Global Currency Support:** Dynamically fetches international rates using the Open Exchange Rates API.
* **Modern UI:** Dark-mode interface using styled Tkinter elements.
* **Input Validation:** Built-in exception handling to prevent crashes from invalid numbers or empty fields.
* **Smart Auto-Detection:** Scans your computer's USB layer for hardware identifiers (VID/PID) to automatically find the Arduino on Windows, macOS, or Linux without manual port configuration.

---

## Software Setup (Python)

**1. Clone the repository and navigate inside:**
git clone https://github.com/swezxyCode/Currency-Converter-Advanced.git
cd Currency-Converter-Advanced

**2. Create a virtual environment and install requirements:**
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt

*(Note for Linux users: If your system lacks Tkinter, install it via: sudo apt install python3-tk)*

**3. Launch the Application:**
python main.py

*The GUI app works standalone. If no hardware is plugged in, it skips the serial connection so you can use the desktop converter normally without crashing.*

---

## Hardware Setup

To use the desktop layout alongside a physical display tracker, follow these steps:

### 1. Hardware Connections
* Connect a 16x2 LCD with an I2C module to your Arduino board.
* **Wiring:** * VCC -> 5V
  * GND -> GND
  * SDA -> A4
  * SCL -> A5
* Open sketch_connecting.ino in the Arduino IDE, install the LiquidCrystal_I2C library, and flash your board.

### 2. Operating System Configurations

* **Windows & macOS:** No extra configuration required. The Python script will instantly identify the communication channel.
* **Linux (Ubuntu/Debian):** Linux restricts raw USB serial writing by default. Run this command to grant your user account access to the serial interface without needing root permissions:
  ```bash
  sudo usermod -a -G dialout $USER
