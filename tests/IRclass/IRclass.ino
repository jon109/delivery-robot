class IR {
private:
  byte m_pin;
  int maxWhiteValue=45;
public:
  void set_pin(byte pin);
  bool IsWhite();
  bool IsBlack();
};

void IR::set_pin(byte pin) {
  m_pin = pin;
}
bool IR::IsWhite() {
  return analogRead(m_pin) < maxWhiteValue;
}
bool IR::IsBlack() {
  return analogRead(m_pin) > maxWhiteValue;
}

IR IR1()
void setup() {
  // put your setup code here, to run once:
  IR1.set_pin(A0)
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("is white: ")
  Serial.println(IR1.IsWhite());
  delay(1000);
}
