int Case13() {
  if (cases == 13) {
    while (1) {
      PidRead();
      while (sensor[0] > 600 && sensor[1] > 600  && sensor[2] > 600 && sensor[3] > 600 && sensor[4] > 600 && sensor[5] > 600  && sensor[6] > 600 && sensor[7] > 600) {
        MotorSpeed(45,35);
        leftMaxSpeed = 50;
        rightMaxSpeed = 50;
        PidRead();
        yenizaman = millis();
      }

      while (sensor[0] < 300 || sensor[1] < 300 || sensor[2] < 300 || sensor[3] < 300 || sensor[4] < 300 || sensor[5] < 300 || sensor[6] < 300 || sensor[7] < 300) {
        Pid();
        if (millis() - yenizaman > 1000) {
          leftMaxSpeed = 200;
          rightMaxSpeed = 200;
       k=1;
          break;
        }
      }
     if(k==1){
      
      break;
     }
    }
  }
}
