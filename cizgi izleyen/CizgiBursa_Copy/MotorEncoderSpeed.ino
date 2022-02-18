
void MotorEncoderSpeed(int DistMillis, int ExSpeed){

int wayTime=0;
float ref=1.6;  //extraspeed=40 için ref=1.8;  //extraspeed=70 için ref=1.6; //extraspeed=100 için ref=1.72;

  
  while(1){
    Pid();
    timeMillis= millis();
    if(timeMillis-exTimeMillis>100){
      extraSpeed=ExSpeed;
      Pid();
      wayTime=wayTime+1;
         if(wayTime==DistMillis){
            MotorSpeed(0,0);
            delay(50);
            break;
          }
     exTimeMillis=timeMillis;
    }  
  }
  extraSpeed=0;
}
