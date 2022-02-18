
int Case7() {
  if (cases == 7) {
    while (1) {
      PidRead();
      MotorSpeed(70, 70);
      if (sensor[7] >600 && sensor[6]>600 && sensor[5]>600 && sensor[4]>600 && sensor[3]>600 && sensor[2]>600 && sensor[1]>600 && sensor[0]>600) {
        break;
      }
    }

    while (1) {
      PidRead();
      MotorSpeed(50, -20);
      if (sensor[6] < 300||sensor[5]<300 ) {
    
        break;
      }
    }
  }
}
