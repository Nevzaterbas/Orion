
int Case15(){
  if(cases==15){
    int obj;
    int objCase=0;
    extraSpeed=0;
    int eskizaman,yenizaman,durum=0;
    extraSpeed=-20;
    Pid();
    if(sensor[0]>600 &&sensor[1]>600 &&sensor[2]>600 && sensor[3]>600 && sensor[4]>600 && sensor[5]>600&& sensor[6]>600&& sensor[7]>600){
      while(1){
        obj=digitalRead(digitalSensor);
        MotorSpeed(30,10);
        if(obj==HIGH){
          break;
        }
      }
    }
    while(sensor[0]>600 &&sensor[1]>600 &&sensor[2]>600 && sensor[3]>600 && sensor[4]>600 && sensor[5]>600&& sensor[6]>600&& sensor[7]>600){
      
        obj=digitalRead(digitalSensor);
        while(obj==HIGH){
        MotorSpeed(40,40);
        obj=digitalRead(digitalSensor);
        PidRead();
        if(sensor[0]<300||sensor[1]<300||sensor[2]<300||sensor[3]<300||sensor[4]<300||sensor[5]<300||sensor[6]<300||sensor[7]<300){
          eskizaman=millis();
          yenizaman=eskizaman;
            break;
          }
        }
        while(obj==LOW){
         MotorSpeed(10,40);
          obj=digitalRead(digitalSensor);
          PidRead();
          
          if(sensor[0]<300||sensor[1]<300||sensor[2]<300||sensor[3]<300||sensor[4]<300||sensor[5]<300||sensor[6]<300||sensor[7]<300){
            eskizaman=millis();
            yenizaman=eskizaman;
            break;
          }
        }
      }

       while(1){
      Pid();
      eskizaman=millis();
      if(eskizaman-yenizaman>350){
        durum=1;
        yenizaman=eskizaman;
      }
      if(durum==1 &&sensor[3]<200 && sensor[4]<200){
        durum=0;
          extraSpeed=70;
        break;
      }
    }

      
  }
}
