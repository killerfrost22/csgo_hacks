#include <Mouse.h>

// const int buttonPin = 28u;  // Set a button to any pin

void setup()
{
  pinMode(buttonPin, INPUT);  // Set the button as an input
  // digitalWrite(buttonPin, HIGH); 
  Serial.begin(9600);
  Mouse.begin(); //Init keyboard emulation
}

void loop()
{
  char read = Serial.read();
  if(read == '<'){
    int x = 0;
    int y = 0;
    Serial.readBytes((char*)&x, 4);
    Serial.readBytes((char*)&y, 4);
    if(Serial.read() == '>')
    {
      // Uncomment this if you want to create a custom button to enable or disable mouse movement
      // if(digitalRead(buttonPin) == HIGH)
        Mouse.move((int)x, (int)y,0);
    }
  } else if (read == '^'){
    Mouse.press();
    delay(10);
    Mouse.release();
  }

  delay(10);  
}
