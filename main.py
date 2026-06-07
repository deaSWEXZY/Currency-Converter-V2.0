import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import design_config as cfg
from design_config import TEXT_LIGHT, FONT_RESULT
import serial
import serial.tools.list_ports
import time

class CurrencyConverterApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Currency Exchange")
        self.root.geometry("300x400")
        self.root.config(bg=cfg.BG_DARK)

        #Icon - Image
        icon_img = Image.open("images/currency.png") #Loading the image file
        self.window_icon = ImageTk.PhotoImage(icon_img) #Converting into Tkinter object
        self.root.iconphoto(False, self.window_icon) #Apply it specifically to the title bar icon slot

        self.rates_data = {}
        # ---------------- ARDUINO INITIALIZATION ----------------
        try:
            self.arduino_port = None
             # ---------------- PORT CHECKING ----------------
            self.TARGET_VIDS = [0x2341, 0x1A86, 0x10C4, 0x0403]

            self.ports = serial.tools.list_ports.comports()

            for port in self.ports:
                if port.vid in self.TARGET_VIDS:
                    print(f"Device: {port.device}")
                    print(f"HEX VID: {port.vid:04X} | PID: {port.pid:04X}")

                    # Open the serial port connection once at startup
                    self.arduino = serial.Serial(port.device, 9600, timeout=1)
                    print("Arduino connection established!")
                    time.sleep(2)
                    break
        except Exception as e:
            print(f"Could not connect to Arduino: {e}")
            self.arduino = None

        self.create_widgets()


        self.fetch_live_data()

    def create_widgets(self):

        title_text = tk.Label(
            self.root,
            text="CURRENCY CONVERTER",
            font=cfg.FONT_TITLE,
            bg=cfg.BG_DARK,
            fg=cfg.ACCENT_COLOR,
        )

        title_text.grid(row=0, column=0, columnspan=2, pady=20)


        """Labels - User Input"""

        # Amount
        amount_label = tk.Label(self.root, text="Amount:", font=cfg.FONT_LABEL, bg=cfg.BG_DARK, fg=TEXT_LIGHT)
        amount_label.grid(row=1, column=0, pady=5)

        # ADDED SELF HERE so the engine can read what the user types
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, pady=5)

        # From
        from_currency_label = tk.Label(self.root, text="From:", font=cfg.FONT_LABEL, bg=cfg.BG_DARK, fg=TEXT_LIGHT)
        from_currency_label.grid(row=2, column=0, pady=5)

        # ADDED SELF HERE so the math engine knows what currency is selected
        self.from_currency_box = ttk.Combobox(self.root)
        self.from_currency_box.grid(row=2, column=1, pady=5)

        # To
        to_currency_label = tk.Label(self.root, text="To:", font=cfg.FONT_LABEL, bg=cfg.BG_DARK, fg=TEXT_LIGHT)
        to_currency_label.grid(row=3, column=0, pady=5)

        self.to_currency_box = ttk.Combobox(self.root)
        self.to_currency_box.grid(row=3, column=1)

        # Result
        result_exchange_label = tk.Label(self.root, text="Result:", font=cfg.FONT_LABEL, bg=cfg.BG_DARK, fg=TEXT_LIGHT)
        result_exchange_label.grid(row=4, column=0, pady=10)

        self.result_exchange_output = tk.Label(self.root, text="--", font=cfg.FONT_LABEL, bg=cfg.BG_DARK, fg=TEXT_LIGHT)
        self.result_exchange_output.grid(row=4, column=1)

        # Button - Convert 
        self.convert_button = ttk.Button(self.root, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=5, column=0, columnspan=2, pady=20)

    def fetch_live_data(self):
        response = requests.get("https://open.er-api.com/v6/latest/USD")

        if response.status_code == 200:
            data_dictionary = response.json()
            self.rates_data = data_dictionary["rates"]

            currency_codes = list(self.rates_data.keys())
            self.from_currency_box['values'] = currency_codes
            self.to_currency_box['values'] = currency_codes

            # ---------------- SEND DATA TO ARDUINO ----------------
            # Check if connection is alive and AMD exists in the API response
            if self.arduino and "AMD" in self.rates_data:
                try:
                    amd_rate = self.rates_data["AMD"]
                    
                    # Format as string with newline, encode to bytes
                    message = f"{amd_rate:.2f}\n"
                    self.arduino.write(message.encode('utf-8'))
                    print(f"Successfully sent USD/AMD to LCD: {amd_rate:.2f}")
                except Exception as e:
                    print(f"Failed to send data to hardware: {e}")

    
    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency_box.get()
            to_curr = self.to_currency_box.get()

            rate_from = self.rates_data[from_curr]
            rate_to = self.rates_data[to_curr]

            final_value = amount * (rate_to / rate_from)

            self.result_exchange_output.config(text=f"{final_value:.2f} {to_curr}", font=FONT_RESULT)

            # ---------------- DYNAMIC ARDUINO UPDATE ----------------
            if self.arduino:
                try:
                    # Format: "100.0 USD|-> 38850.00 AMD\n"
                    lcd_text = f"{amount} {from_curr}|-> {final_value:.2f} {to_curr}\n"
                    self.arduino.write(lcd_text.encode('utf-8'))
                    print(f"Sent to LCD: {lcd_text.strip()}")
                except Exception as e:
                    print(f"Failed to send data to hardware: {e}")

        except KeyError:
            messagebox.showwarning(title="Error", message="Select valid currency")
        except ValueError:
            messagebox.showwarning(title="Error", message="Enter a number please.")



root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()
