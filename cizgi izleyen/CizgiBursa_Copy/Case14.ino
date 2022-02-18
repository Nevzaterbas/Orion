int Case14() {
  if (cases == 14) {
    while (1) {
      MotorSpeed(-80, -50);
      PidRead();
      if (sensor[7] > 600 && sensor[6] > 600) {
        break;
      }
    }

    while (1) {
      PidRead();
      MotorSpeed(-50, 60);
      if (sensor[6] < 300 || sensor[7] < 300) {
      
        break;
      }
    }
  }
}
