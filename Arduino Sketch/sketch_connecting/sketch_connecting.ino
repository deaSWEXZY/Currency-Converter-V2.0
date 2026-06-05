#include <Wire.h>
#include <LiquidCrystal_I2C.h> 

// Initialize the LCD. Address is usually 0x27 or 0x3F for a 16x2 screen
LiquidCrystal_I2C lcd(0x27, 16, 2); 

void setup() {
  // Start the serial connection at the same baud rate as your Python script
  Serial.begin(9600);
  
  // Initialize the LCD and turn on the backlight
  lcd.init();
  lcd.backlight();
  
  // Print the initial connecting message
  lcd.setCursor(0, 0);
  lcd.print("Connecting...");
}

void loop() {
  // Check if Python has sent any data down the USB cable
  if (Serial.available() > 0) {
    
    // Read the incoming bytes until the newline (\n) arrives
    String incomingRate = Serial.readStringUntil('\n');
    
    // Clean up any accidental invisible characters or spaces
    incomingRate.trim(); 

    // Wipe the screen and print the new data
    lcd.clear();                  
    lcd.setCursor(0, 0);          
    lcd.print("USD to AMD:");
    
    lcd.setCursor(0, 1);          
    lcd.print(incomingRate);      
  }
}