
int Case5() {
  if (cases == 5) {
    while (1) {
      PidRead();
      MotorSpeed(70, 70);
      if (sensor[7] > 600 && sensor[6] > 600 && sensor[5] > 600 && sensor[4] > 600 && sensor[3] > 600 && sensor[2] > 600 && sensor[1] > 600 && sensor[0] > 600) {
        break;
      }
    }

    while (1) {
      PidRead();
      MotorSpeed(-30, 50);
      if (sensor[4] < 300 || sensor[5] < 300) {
      Pid();
        break;
      }
    }
  }
}
