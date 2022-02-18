
void MotorBrake(int delay){
int i=0;
  for(i; i=delay; i++){
    if(i%2==0){
      MotorSpeed(0,0);
      //delay(1);
    }
    if(i%2==1){
      MotorSpeed(350,350);
      //delay(1);
    }
  }
}
