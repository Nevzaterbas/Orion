
void Calibration(){
  
//  Serial.println(error);
  int left=0, right=0;
  for(int calibrationCase=0;calibrationCase<7;calibrationCase++){
   while(analogRead(A0)>600){
    qtr.calibrate();
    MotorSpeed(-25,25);
   }
   while(analogRead(A7)>600){
    qtr.calibrate();
    MotorSpeed(25,-25);
   }
  }

  while(1){
    MotorSpeed(-20,20); 
    if( (analogRead(A3)<250 && analogRead(A4)<250) || (analogRead(A5)<250 && analogRead(A4)<250)  ){
      MotorSpeed(0,0);
      delay(500);
      break;
    }
  }
  
  
}
