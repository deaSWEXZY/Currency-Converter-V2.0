#include <Wire.h>
#include <LiquidCrystal_I2C.h> 

// Initialize the LCD. Address is usually 0x27 or 0x3F for a 16x2 screen
LiquidCrystal_I2C lcd(0x27, 16, 2); 

const int BUZZER_PIN = 13;
const int BUTTON_PIN = 7;

String currentBaseRate = "---";

void setup() {
  // Start the serial connection at the same baud rate as your Python script
  Serial.begin(9600);
  
  // Initialize the LCD and turn on the backlight
  lcd.init();
  lcd.backlight();

  //Buzzer
  pinMode(13, OUTPUT);

  //Button

  // Configure pin as input and enable the internal pullup resistor
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Print the initial connecting message
  lcd.setCursor(0, 0);
  lcd.print("Connecting...");
  
}

void loop() {
  
  if (digitalRead(BUTTON_PIN) == HIGH) {
        triggerManualReset();
  }

  if (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n'); // Rates from API
    incomingData.trim();
    
    int separatorIndex = incomingData.indexOf('|');

    // Check if Python sent a Reset Command
    if (incomingData == "HARDWARE_RESET") {
      triggerManualReset();
      return; 
    }

    if (separatorIndex > 0) {
      String topRow = incomingData.substring(0, separatorIndex); 
      String bottomRow = incomingData.substring(separatorIndex + 1); 

      // DEFENSIVE: Force it to never exceed 16 characters
      if (topRow.length() > 16) { topRow = topRow.substring(0, 16); }
      if (bottomRow.length() > 16) {bottomRow = bottomRow.substring(0, 16);}

      displayCustomMessage(topRow, bottomRow, 2000, 300);
    }

    else {
      currentBaseRate = incomingData; 
      showDefaultState();
      tone(BUZZER_PIN, 2000, 300);
    }
  }
}

// ------------------ DEDICATED RESET FUNCTION ------------------
void triggerManualReset() {
  lcd.clear();
  delay(10); // Clear stability delay
  
  lcd.setCursor(0, 0);
  lcd.print("Manual Reset...");
  lcd.setCursor(0, 1);
  lcd.print("Ready.");
  
  tone(BUZZER_PIN, 1500, 100);
  
  // Inform your Python script over serial terminal link
  Serial.println("HARDWARE_RESET"); 
  
  delay(400); // Debounce delay to prevent click stuttering
}

//  ------------------ DEFAULT STATE ------------------
void showDefaultState() {
  lcd.clear();
  delay(10);
  lcd.setCursor(0, 0);
  lcd.print("USD / AMD Rate: ");
  lcd.setCursor(0, 1);
  lcd.print(currentBaseRate + " AMD");
}

//  ------------------ OUTPUT TEXT WRAPPER ------------------
void displayCustomMessage(String line1, String line2, int frequency, int duration) {
  lcd.clear();                  
  delay(10); 
  lcd.setCursor(0, 0);          
  lcd.print(line1);
  lcd.setCursor(0, 1);          
  lcd.print(line2);
  
  if (frequency > 0) {
    tone(BUZZER_PIN, frequency, duration);
  }
}
