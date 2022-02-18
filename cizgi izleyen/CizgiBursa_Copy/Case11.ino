
int Case11(){
  if(cases==11){
    while(1){
      MotorSpeed(70,70);
      PidRead();
      if(sensor[0]>600 && sensor[7]>600){
        break;
      }
    }
  }
}
