#include "Arduino.h"
#include "help_classes.h"
//ir value that will be considered a gray/black point

void IR::set_pin(byte pin) {
  m_pin = pin;
}
bool IR::IsWhite() {
  return analogRead(m_pin) < maxWhiteValue;
}
bool IR::IsBlack() {
  return analogRead(m_pin) > maxWhiteValue;
}

void IR::printIR(char Name) {
  if (IsBlack())
  {
    Serial.print(Name);
    Serial.print(" Is black.");
  }
  else if (IsWhite())
  {
    Serial.print(Name);
    Serial.print(" Is white.");
  }
}
