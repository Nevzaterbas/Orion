int Case12() {
  if (cases == 12) {
    while (1) {
      MotorSpeed(-80, -50);
      PidRead();
      if (sensor[0] > 600 && sensor[1] > 600) {
        break;
      }
    }

    while (1) {
      PidRead();
      MotorSpeed(-50, 60);
      if (sensor[0] < 300 || sensor[1] < 300) {
      
        break;
      }
    }
  }
}
