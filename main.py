from tkinter import messagebox, Tk
from PIL import Image, ImageTk
import requests
import design_config as cfg
from design_config import TEXT_LIGHT, FONT_RESULT
import serial
import serial.tools.list_ports
import time
import customtkinter as tkc #Updated Tkinter

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("300x400")
        self.root.config(bg=cfg.BG_DARK)
        self.root.resizable(False, False) #Make Sure that it's not resizable!

        #Icon - Image
        icon_img = Image.open("images/currency.png") #Loading the image file
        self.window_icon = ImageTk.PhotoImage(icon_img) #Converting into Tkinter object
        self.root.iconphoto(False, self.window_icon) #Apply it specifically to the title bar icon slot

        self.rates_data = {}
        self.arduino = None # Starting With None State

        # ---------------- START BLOCK ----------------
        messagebox.showinfo(title="Read README for Arduino!!",message="Hello, dear user!\nPlease read instructions for Arduino LCD\nIf you have one.\nThank You!!")

        # ---------------- ARDUINO INITIALIZATION ----------------
        try:
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
            if self.arduino is None:
                print("Connect Arduino.. No valid hardware found on any port.")

        except Exception as e:
            print(f"Could not connect to Arduino: {e}")
            self.arduino = None
        self.create_widgets()
        self.fetch_live_data()

        self.check_serial_trigger()

    def create_widgets(self):
        #Centering Columns
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        title_text = tkc.CTkLabel(
            self.root,
            text="CURRENCY CONVERTER",
            font=cfg.FONT_TITLE,
            text_color=cfg.ACCENT_COLOR
        )

        #------------------ ELEMENTS ON GRID ------------------

        # Amount
        amount_label = tkc.CTkLabel(self.root, text="Amount:", font=cfg.FONT_LABEL, text_color=TEXT_LIGHT)

        # ADDED SELF HERE so the engine can read what the user types
        self.amount_entry = tkc.CTkEntry(self.root)

        # From
        from_currency_label = tkc.CTkLabel(self.root, text="From:", font=cfg.FONT_LABEL, text_color=TEXT_LIGHT)
        self.from_currency_box = tkc.CTkComboBox(self.root)
        self.from_currency_box.set("USD")

        # To
        to_currency_label = tkc.CTkLabel(self.root, text="To:", font=cfg.FONT_LABEL, text_color=TEXT_LIGHT)
        self.to_currency_box = tkc.CTkComboBox(self.root)
        self.to_currency_box.set("AMD")

        # Result
        result_exchange_label = tkc.CTkLabel(self.root, text="Result:", font=cfg.FONT_LABEL, text_color=TEXT_LIGHT)

        self.result_exchange_output = tkc.CTkLabel(self.root, text="--", font=cfg.FONT_LABEL, text_color=TEXT_LIGHT)

        # Button - Convert
        self.convert_button = tkc.CTkButton(
            self.root,
            text="Convert",
            command=self.convert_currency,
            fg_color=cfg.BUTTON_COLOR,
            hover_color=cfg.BUTTON_HOVER
        )

        # Button - Reset
        self.reset_button = tkc.CTkButton(
            self.root,
            text="Reset",
            fg_color=cfg.BUTTON_COLOR,
            hover_color=cfg.BUTTON_HOVER,
            command=self.reset_input
        )

        #------------------ ELEMENTS PLACING ------------------

        # Title
        title_text.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Amount
        amount_label.grid(row=1, column=0, pady=5, padx=(0, 10), sticky="e")
        self.amount_entry.grid(row=1, column=1, pady=5, sticky="w")

        # From
        from_currency_label.grid(row=2, column=0, pady=5, padx=(0, 10), sticky="e")
        self.from_currency_box.grid(row=2, column=1, pady=5, sticky="w")

        # To
        to_currency_label.grid(row=3, column=0, pady=5, padx=(0, 10), sticky="e")
        self.to_currency_box.grid(row=3, column=1, pady=5, sticky="w")

        # Result
        result_exchange_label.grid(row=4, column=0, pady=10, padx=(0, 10), sticky="e")
        self.result_exchange_output.grid(row=4, column=1, pady=10, sticky="w")

        # Button (Centered across both columns)
        self.convert_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Button - Reset
        self.reset_button.grid(row=6, column=1, pady=20)

    #------------------ LIVE API DATA ------------------
    def fetch_live_data(self):
        response = requests.get("https://open.er-api.com/v6/latest/USD")

        if response.status_code == 200:
            data_dictionary = response.json()
            self.rates_data = data_dictionary["rates"]

            currency_codes = list(self.rates_data.keys())
            self.from_currency_box.configure(values=currency_codes)
            self.to_currency_box.configure(values=currency_codes)

            if self.arduino and "AMD" in self.rates_data:
                self.start_state() # start_state function is USD / AMD Rate

    # ---------------- SEND START STATE DATA TO ARDUINO ----------------
    def start_state(self):
        try:
            amd_rate = self.rates_data["AMD"]

            # Format as string with newline, encode to bytes
            message = f"{amd_rate:.2f}\n"
            self.arduino.write(message.encode('utf-8'))
            print(f"Successfully sent USD/AMD to LCD: {amd_rate:.2f}")

        except Exception as e:
            print(f"Failed to send data to hardware: {e}")

    #------------------ MAIN LOGIC(CONVERTING) ------------------
    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency_box.get()
            to_curr = self.to_currency_box.get()

            rate_from = self.rates_data[from_curr]
            rate_to = self.rates_data[to_curr]

            final_value = amount * (rate_to / rate_from)

            self.result_exchange_output.configure(text=f"{final_value:.2f} {to_curr}", font=FONT_RESULT)

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

        # ------------------ MANUAL RESET ------------------
    def check_serial_trigger(self):
        # Only check if the serial connection is open
        if self.arduino and self.arduino.in_waiting > 0:
            try:
                # Read line the Arduino printed
                incoming_signal = self.arduino.readline().decode('utf-8').strip()

                if incoming_signal == "HARDWARE_RESET":
                    print("[Hardware Event] Physical button pressed! Resetting UI...")
                    # Trigger UI reset function
                    self.reset_input()

            except Exception as e:
                print(f"Error reading serial event: {e}")

        # Schedule Python to run this check function again in 100ms
        self.root.after(100, self.check_serial_trigger)

    # ------------------ RESET ALL ------------------
    def reset_input(self):
        self.result_exchange_output.configure(text="--")
        self.amount_entry.delete(0, "end")
        self.from_currency_box.set("RUB")
        self.to_currency_box.set("AMD")

        if self.arduino:
            try:
                reset_message = "System Reset... |Ready\n"
                self.arduino.write(reset_message.encode('utf-8'))
                print("Sent reset command to Arduino LCD.")
                self.root.after(1000, self.start_state)

            except Exception as e:
                print(f"Failed to clear hardware display: {e}")

#------------------ OBJECTS - THE END ------------------
root = Tk()
app = CurrencyConverterApp(root)
root.mainloop()
