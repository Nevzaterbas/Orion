
int Case6() {
  if (cases == 6) {
    while (1) {

      PidRead();
      MotorSpeed(70, 70);
      if (sensor[7] > 600 && sensor[6] > 600 && sensor[0] > 600 && sensor[1] > 600 ) {

        break;
      }
    }
  }
}
