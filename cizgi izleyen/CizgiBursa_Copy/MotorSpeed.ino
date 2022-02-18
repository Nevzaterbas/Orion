void MotorSpeed(int c, int s){

  if(c>0){
    analogWrite(LeftMotorPWM,c);
    digitalWrite(LeftMotor1,1);
    digitalWrite(LeftMotor2,0);
  }
  else if(c<0){
    analogWrite(LeftMotorPWM,abs(c));
    digitalWrite(LeftMotor1,0);
    digitalWrite(LeftMotor2,1);
  }
  else if(c==0){
    analogWrite(LeftMotorPWM,200);
    digitalWrite(LeftMotor1,1);
    digitalWrite(LeftMotor2,1);
  }
  else if(c==350){
    analogWrite(LeftMotorPWM,0);
    digitalWrite(LeftMotor1,0);
    digitalWrite(LeftMotor2,0);
  }

  if(s>0){
    analogWrite(RightMotorPWM,s);
    digitalWrite(RightMotor1,1);
    digitalWrite(RightMotor2,0);
  }
  else if(s<0){
    analogWrite(RightMotorPWM,abs(s));
    digitalWrite(RightMotor1,0);
    digitalWrite(RightMotor2,1);
  }
  else if(s==0){
    analogWrite(RightMotorPWM,200);
    digitalWrite(RightMotor1,1);
    digitalWrite(RightMotor2,1);
  }
  else if(s==350){
    analogWrite(RightMotorPWM,0);
    digitalWrite(RightMotor1,0);
    digitalWrite(RightMotor2,0);
  }
}
