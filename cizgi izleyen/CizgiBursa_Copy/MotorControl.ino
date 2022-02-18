
void RightForward(int c){
  analogWrite(RightMotorPWM,c);
  digitalWrite(RightMotor1,1);
  digitalWrite(RightMotor2,0);
}

void RightBack(int c){
  analogWrite(RightMotorPWM,c);
  digitalWrite(RightMotor1,0);
  digitalWrite(RightMotor2,1);
}

void LeftForward(int c){
  analogWrite(LeftMotorPWM,c);
  digitalWrite(LeftMotor1,1);
  digitalWrite(LeftMotor2,0);
}

void LeftBack(int c){
  analogWrite(LeftMotorPWM,c);
  digitalWrite(LeftMotor1,0);
  digitalWrite(LeftMotor2,1);
}
