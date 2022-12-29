#include "help_classes.h"
#define HI 255
#define MID 60
//motor
byte m_in1;
byte m_in2;
byte m_in3;
byte m_in4;
//IR
IR m_leftIR;   // left
IR m_rightIR;  // right
IR m_middleIR; // middle
//General varibels
byte current_direction = 0;  // north=0,east=90,south=180,west=270
byte positon[2] = { 0, 0 };  //[x,y] car starts at bottom left corner facing up(north)
long lastIntersectionTime = millis();

// ================================================================
// ===             initializers for motors and IRs              ===
// ================================================================

void motor_init(byte in1, byte in2, byte in3, byte in4) {
  m_in1 = in1;
  m_in2 = in2;
  m_in3 = in3;
  m_in4 = in4;
  pinMode(m_in1, OUTPUT);
  pinMode(m_in2, OUTPUT);
  pinMode(m_in3, OUTPUT);
  pinMode(m_in4, OUTPUT);
}

void IR_init(byte leftIR, byte middleIR, byte rightIR) {
  m_leftIR.set_pin(leftIR);
  m_rightIR.set_pin(rightIR);
  m_middleIR.set_pin(middleIR);
  pinMode(leftIR, INPUT);
  pinMode(rightIR, INPUT);
  pinMode(middleIR, INPUT);
}

// ================================================================
// ===                 simple motor functions                   ===
// ================================================================

void Forward() {
  analogWrite(m_in1, MID);
  analogWrite(m_in2, LOW);
  analogWrite(m_in3, MID);
  analogWrite(m_in4, LOW);
}

void Backward() {
  analogWrite(m_in1, LOW);
  analogWrite(m_in2, MID);
  analogWrite(m_in3, LOW);
  analogWrite(m_in4, MID);
}

void Stop() {
  analogWrite(m_in1, LOW);
  analogWrite(m_in2, LOW);
  analogWrite(m_in3, LOW);
  analogWrite(m_in4, LOW);
}

void Right() {
  analogWrite(m_in1, LOW);
  analogWrite(m_in2, LOW);
  analogWrite(m_in3, MID);
  analogWrite(m_in4, LOW);
}

void Left() {
  analogWrite(m_in1, MID);
  analogWrite(m_in2, LOW);
  analogWrite(m_in3, LOW);
  analogWrite(m_in4, LOW);
}

void Mixed() {
  analogWrite(m_in1, LOW);
  analogWrite(m_in2, MID);
  analogWrite(m_in3, MID);
  analogWrite(m_in4, LOW);
}

// ================================================================
// ===                 follow grid functions                    ===
// ================================================================

bool IsIntersection() {
  return m_middleIR.IsBlack() && m_leftIR.IsBlack() && m_rightIR.IsBlack();  // for now we
}
/*void turn(byte end_direction)  // we might need to use adxl to make this more presice
  {
  byte turning_time = 200;
  byte turning_angle;

  if (end_direction - current_direction > 0)
    turning_angle = end_direction - current_direction;
  else
    turning_angle = end_direction - current_direction + 360;

  if (turning_angle == 90)  // right turn
  {
    Right();
    delay(turning_time);
  }
  if (turning_angle == 270)  // left turn
  {
    Left();
    delay(turning_time);
  }
  if (turning_angle == 180)  // 180 degree turn
  {
    Right();
    delay(2 * turning_time);
  }

  // update direction
  current_direction = (current_direction + turning_angle) % 360;
  }*/

//this functions needs to be completly changed, so it uses gyro and PID and IRs
//this function should make it so the robot always moves in a straight line
//even without the blackline
//but if does cross the black line it will correct it self
void FollowBlackLineGyro()
{
  // maybe we should add delay
  if (m_leftIR.IsBlack() && m_rightIR.IsWhite()) {
    Left();
  } else if (m_leftIR.IsWhite() && m_rightIR.IsBlack()) {
    Right();
  } else {
    //Forward();
    SmartForward2(computePID(current_direction));
  }
}

void FollowBlackLineIR()
{
  // maybe we should add delay
  if (m_leftIR.IsBlack() && m_rightIR.IsWhite()) {
    Left();
  } else if (m_leftIR.IsWhite() && m_rightIR.IsBlack()) {
    Right();
  } else {
    Forward();
    //SmartForward2(computePID(current_direction));
  }
}

void printIR2() {
  m_leftIR.printIR(' ');
  m_middleIR.printIR('  ');
  m_rightIR.printIR(' ');
  Serial.println();
}


void ForwardByTiles(int distance) {
  byte tiles = 0;
  while (tiles < distance) {
    FollowBlackLineIR();
    if (IsIntersection()) {
      digitalWrite(13, HIGH);
      delay(20);
      digitalWrite(13, LOW);
      delay(20);
      digitalWrite(13, HIGH);
      delay(20);
      digitalWrite(13, LOW);
      delay(20);
      if (millis() - lastIntersectionTime >= 300)
      {
        lastIntersectionTime = millis();
        tiles += 1;
        Serial.println("ÄAA");
        FollowBlackLineIR();  // blackline might not work on intersection
        delay(50);
      }
    }
  }
  // update position
  if (current_direction == 0)
    positon[1] += distance;
    if (current_direction == RIGHT)


    
    positon[0] += distance;
    if (current_direction == BACK)
    positon[1] -= distance;
    if (current_direction == LEFT)
    positon[0] -= distance;
}

void Move(int arr[][2]) {
  //for (int i = 0; i < sizeof(arr) / sizeof(arr[1]); i++) {
  for (int i = 0; i < 6; i++) {
    SmartTurn(arr[i][0]);
   // current_direction += arr[i][0];
    //current_direction -= floor((current_direction + 180) / 360) * 360;
    delay(50);
    current_direction = mpu_get_yaw();
    ForwardByTiles(arr[i][1]);
  }
}
