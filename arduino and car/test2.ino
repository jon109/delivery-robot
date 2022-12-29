//PID constants
/*double Ku = 0.01;
  double Tu = 6;

  double Kp = 0.20 * Ku;
  double Ki = 0.40 * Ku / Tu;
  double Kd = 0.066 * Ku * Tu;*/

double Kp = 2.5;
double Ki = 0.0075;
double Kd = 1300; // Right, not a mistake.

unsigned long currentTime = 0, previousTime = 0;
double elapsedTime = 0;
double error = 0;
double lastError = 0;
double input = 0, output = 0;
double cumError = 0, rateError = 0;

double computePID(double Setpoint) {
  currentTime = millis();      //get current time
  elapsedTime = (double)(currentTime - previousTime);        //compute time elapsed from previous computation
  double yaw = mpu_get_yaw();
  error = Setpoint - yaw;
  Serial.println(error);
  error -= floor((error + 180) / 360) * 360;
  if (abs(error) < 0.5) cumError = 0;
  if (abs(error) < 0.5) return 0;
  // determine error
  cumError += error * elapsedTime;                // compute integral
  rateError = (error - lastError) / elapsedTime; // compute derivative
  double out = Kp * error + Ki * cumError + Kd * rateError;          //PID output
  lastError = error;                                //remember current error
  previousTime = currentTime;
  /*Serial.print("      out:");//remember current time
    Serial.print(out/2);*/
  return out;                                        //have function return the PID output
}
double rightValue = 60;
double leftValue = 60;
/*void SmartForward1(double change)
  {
  error = Setpoint - mpu_get_yaw();
  if (abs(error) < 3);
  else
  {
    if (error > 15)
    {
      change = 15 ;
      SmartForward2(change);
    }
    else if (error < -15)
    {
      change = -15;
      SmartForward2(change);
    }
    else
    {
      SmartForward2(error*Kp);
    }
  }
  }*/
void SmartForward2(double change) {
  change /= -2;
  if (rightValue + change > 128) rightValue = 128;
  else if (rightValue + change < 0) rightValue = 60;
  else rightValue += change;
  if (leftValue - change > 128) leftValue = 128;
  else if (leftValue - change < 0) leftValue = 60;
  else leftValue -= change;
  analogWrite(5, rightValue);
  analogWrite(6, leftValue);
  delay(70);
}

void SmartTurn(int angle) {
  Serial.println("BOOOOOOOOOOOO!");
  if (angle == RIGHT || angle == LEFT)
  {
    Backward();
    delay(300);
    Stop();
    delay(50);
  }
  if (angle == RIGHT)
  {
    SmartRight();
  }
  if (angle == LEFT)
  {
    Serial.println("LEFT!!!!!!");
    SmartLeft();
  }
  if (angle == BACK)
  {
    SmartBackward();
    double initialYaw = mpu_get_yaw();
    analogWrite(m_in1, MID);
    analogWrite(m_in2, LOW);
    analogWrite(m_in3, LOW);
    analogWrite(m_in4, MID);
    delay(50);
    Forward();
    delay(50);
    while (mpu_get_yaw() <= initialYaw)
    {
      Mixed();
    }
  }
}

void SmartRight()
{
  double initialYaw = mpu_get_yaw();
  double yaw = mpu_get_yaw();
  yaw -= floor((yaw + 180) / 360) * 360;
  while (yaw - initialYaw <= RIGHT)
  {
    Right();
    yaw = mpu_get_yaw();
    yaw -= floor((yaw + 180) / 360) * 360;
    //Serial.println(yaw - initialYaw);
  }
}

void SmartLeft()
{
  Serial.println("hello left");
  double initialYaw = mpu_get_yaw();
  double yaw = mpu_get_yaw();
  yaw -= floor((yaw + 180) / 360) * 360;
  while (yaw - initialYaw >= LEFT)
  {
    Left();
    yaw = mpu_get_yaw();
    yaw -= floor((yaw + 180) / 360) * 360;
    //Serial.println(yaw - initialYaw);
  }
}

void SmartBackward()
{
  double initialYaw = mpu_get_yaw();
  double yaw = mpu_get_yaw();
  yaw -= floor((yaw + 180) / 360) * 360;
  while (yaw - initialYaw <= BACK)
  {
    Mixed();
    yaw = mpu_get_yaw();
    yaw -= floor((yaw + 180) / 360) * 360;
    //Serial.println(yaw - initialYaw);
  }
}
