void Pid(){
  
  //int position = qtra.readLine(sensor, 1, zemin);
  uint16_t position = qtr.readLineWhite(sensor);
  int error = position - 3500;

  if (micros() - say > 10000) {
  int motorSpeed = Kp * error + Kd * (error - lastError);
  lastError = error;

  rightMotorSpeed = rightBaseSpeed + motorSpeed + extraSpeed;
  leftMotorSpeed = leftBaseSpeed - motorSpeed + extraSpeed;

  if(rightMotorSpeed>rightMaxSpeed){rightMotorSpeed=rightMaxSpeed;}
  else if(abs(rightMotorSpeed)>rightMaxSpeed){rightMotorSpeed=rightMaxSpeed*(-1);}

  if(rightMotorSpeed<0){
    RightBack(abs(rightMotorSpeed));
    }
   else{
    RightForward(rightMotorSpeed);
   }

  if(leftMotorSpeed>leftMaxSpeed){leftMotorSpeed=leftMaxSpeed;}
  else if(abs(leftMotorSpeed)>leftMaxSpeed){leftMotorSpeed=leftMaxSpeed*(-1);}

  if(leftMotorSpeed<0){
    LeftBack(abs(leftMotorSpeed));
    }
   else{
    LeftForward(leftMotorSpeed);
   }
 say=micros();
 
  }
}
