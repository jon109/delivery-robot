#define IRpin A0
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  double value = analogRead(IRpin);
  Serial.println(value);
  delay(200);
}
