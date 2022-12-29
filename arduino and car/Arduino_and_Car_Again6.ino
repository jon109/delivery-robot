#define FORWARD 0
#define RIGHT 83
#define LEFT -83
#define BACK 167
void setup() {
  motor_init(5, 3, 6, 9);
  IR_init(A2, A1, A0);
  mpu_init();
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  //Serial.begin(9600); //Appears on mpu_init.
}

int arr[6][2] = {{FORWARD, 2}, {RIGHT, 1}, {LEFT, 1}, {BACK, 2}, {RIGHT, 1}, {RIGHT, 1}};
void loop() {
  //printIR2();
  //delay(200);
  //SmartTurn(BACK);
  Move(arr);
  //SmartRight();
  //SmartLeft();
  //ForwardByTiles(1);
  Stop();
  delay(200000);
  //FollowBlackLine();
  /*int x[3][4] = {{0,1,2,3}, {4,5,6,7}, {8,9,10,11}};
    move(arr);*/
  /*if (millis() - lastIntersectionTime >= 1000)
  {
    digitalWrite(13, HIGH);
      delay(20);
      digitalWrite(13, LOW);
      delay(20);
      digitalWrite(13, HIGH);
      delay(20);
      digitalWrite(13, LOW);
      delay(20);
  }*/
}

