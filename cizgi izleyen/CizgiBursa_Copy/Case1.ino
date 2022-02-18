
int Case1(){
  if(cases==1){
      while(1){
      PidRead();
      MotorSpeed(70,70);
      if(sensor[0]>600 && sensor[7]>600){
        //MotorEncoderSpeed(500,0,70);
       
        break;
      }
    }
  }
}
