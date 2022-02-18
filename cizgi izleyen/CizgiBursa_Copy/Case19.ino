
int Case19(){
  if(cases==19){
      while(1){
      PidRead();
      MotorSpeed(120,120);
      if(sensor[0]>600 && sensor[7]>600){
      
MotorBrake(10000);
        break;
      }
    }
  }
}
