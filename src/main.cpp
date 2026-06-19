#include <Arduino.h>
#include <LiquidCrystal.h>

#define RED 2
#define GREEN 3
#define BLUE 4

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setColor(int r, int g, int b) {
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
}

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);

  pinMode(RED, OUTPUT); 
  pinMode(GREEN, OUTPUT); 
  pinMode(BLUE, OUTPUT); 
  
  setColor(0, 0, 0);
  
  lcd.print("Awaiting Model...");
}

void loop() {
  if (Serial.available() > 0) {
    String emotion = Serial.readStringUntil('\n');
    emotion.trim();
    
    if (emotion.length() > 0) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Emotion:");
      lcd.setCursor(0, 1);
      lcd.print(emotion);

      if (emotion == "Neutral") {
        setColor(100, 100, 100); 
      } else if (emotion == "Happy") {
        setColor(0, 255, 0);     
      } else if (emotion == "Surprise") {
        setColor(0, 255, 255);   
      } else if (emotion == "Sad") {
        setColor(0, 0, 255);     
      } else if (emotion == "Anger") {
        setColor(255, 0, 0);     
      } else if (emotion == "Disgust") {
        setColor(50, 255, 0);   
      } else if (emotion == "Fear") {
        setColor(128, 0, 128);   
      } else if (emotion == "Contempt") {
        setColor(255, 50, 0);    
      } else {
        setColor(0, 0, 0);       
      }
    }
  }
}