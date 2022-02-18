
int Case2(){
  if(cases==2){
    while(1){
      PidRead();
      MotorSpeed(70,70);
      if(sensor[0]>600 && sensor[7]>600){
        //MotorEncoderSpeed(1000,50,70);
       
        break;
      }
    }
  }
}
