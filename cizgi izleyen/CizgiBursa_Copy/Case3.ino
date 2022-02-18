
int Case3(){
  if(cases==3){
    while(1){
     PidRead();
      MotorSpeed(70, 70);
      if (sensor[7] <300 ) {
        break;
      }
    }

     while (1) {

      PidRead();
      MotorSpeed(70, 70);
      if (sensor[7] >600 ) {
       extraSpeed=-10;
        break;
      }
    }
    
  
  }
}
