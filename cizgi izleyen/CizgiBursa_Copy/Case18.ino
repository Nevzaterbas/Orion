
int Case18(){
  if(cases==18){
      while(1){
      PidRead();
      MotorSpeed(120,120);
      if(sensor[0]>600 && sensor[7]>600){
      
        break;
      }
    }
  }
}
