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
  if (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n');
    incomingData.trim();
    
    int separatorIndex = incomingData.indexOf('|');
    
    if (separatorIndex > 0) {
      String topRow = incomingData.substring(0, separatorIndex); 
      String bottomRow = incomingData.substring(separatorIndex + 1); 
      
      // DEFENSIVE TRUNCATION: Force it to never exceed 16 characters
      if (topRow.length() > 16) { topRow = topRow.substring(0, 16); }
      if (bottomRow.length() > 16) { bottomRow = bottomRow.substring(0, 16); }
      
      lcd.clear();                  
      delay(10); // I2C bus 10 milliseconds to physically clear

      lcd.setCursor(0, 0);          
      lcd.print(topRow);
      
      lcd.setCursor(0, 1);          
      lcd.print(bottomRow);  
    }
  }
}