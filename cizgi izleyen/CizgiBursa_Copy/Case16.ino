
int Case16(){
  if(cases==16){
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
        break;
      }
    }
  }
}
