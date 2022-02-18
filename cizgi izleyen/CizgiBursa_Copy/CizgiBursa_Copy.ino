// ELEME PİSTİ

#include <QTRSensors.h>

QTRSensors qtr;
#define sensorSayisi  8
int sensor[sensorSayisi];
int durum[8];


#define Kp 0.045
#define Kd 0.650

#define rightBaseSpeed 70//70
#define leftBaseSpeed 70//70

#define RightMotor1 8
#define RightMotor2 9
#define RightMotorPWM 10
#define LeftMotor1 6
#define LeftMotor2 7
#define LeftMotorPWM 5

int rightMaxSpeed = 200;
int leftMaxSpeed = 200;

int rightMotorSpeed;
int leftMotorSpeed;
unsigned long yenizaman;
int digitalSensor = 13;
int timeMillis;
int exTimeMillis;
int extraSpeed;
int calibrationCase;
int motorBrakeCase;
int lastError = 0;
int cases =0;
int first = 0;
int second = 0;
int thirth = 0;
int fourth = 0;
int fifth = 0;
int sixth = 0;
int seventh = 0;
int seventhi = 0;
int eighth = 0;
int nineth = 0;
int tenth = 0;
int led = 0;
uint16_t say;
int test = 0;
int k=0;

void setup() {
  // put your setup code here, to run once:
  qtr.setTypeAnalog();
  qtr.setSensorPins((const uint8_t[]) {
    A7, A6, A5, A4, A3, A2, A1, A0
  }, sensorSayisi);
  //qtr.setEmitterPin(0);
  Serial.begin(9600);

  pinMode(RightMotor1, OUTPUT);
  pinMode(RightMotor2, OUTPUT);
  pinMode(RightMotorPWM, OUTPUT);
  pinMode(LeftMotor1, OUTPUT);
  pinMode(LeftMotor2, OUTPUT);
  pinMode(LeftMotorPWM, OUTPUT);
  pinMode(digitalSensor, INPUT);

  digitalWrite(led, HIGH); delay(120);
  digitalWrite(led, LOW); delay(120);
  digitalWrite(led, HIGH); delay(120);
  digitalWrite(led, LOW); delay(120);
  digitalWrite(led, HIGH); delay(1200);
  Calibration();

  digitalWrite(led, LOW); delay(120);
  digitalWrite(led, HIGH); delay(120);
  digitalWrite(led, LOW); delay(120);
  digitalWrite(led, HIGH); delay(2000);

  Serial.begin(9600);
}

void loop() {

  while (1) {
    Pid();

    // Case0 için;
    if (cases == 0 && (sensor[3] < 200 || sensor[4] < 200) && (sensor[1] < 200 || sensor[0] < 200)) {
      cases = 0;
      break;
    }

    // Case1 için;
    else if (cases == 1 && (sensor[3] < 200 || sensor[4] < 200) && (sensor[1] < 200 || sensor[0] < 200)) {
      cases = 1;
      break;
    }

    // Case2 için;
    else if (cases == 2 &&  (sensor[3] < 200 || sensor[4] < 200) && (sensor[1] < 200 || sensor[0] < 200) ) {
      cases = 2;
      break;
    }

    // Case3 için;
    else if (cases == 3 && (sensor[3] < 200 || sensor[4] < 200) && (sensor[1] < 200 || sensor[0] < 200) ) {
      cases = 3;
      break;
    }

    // Case4 için;
    else if (cases == 4 && (sensor[0] > 600 && sensor[1] > 600  && sensor[2] > 600 && sensor[3] > 600 && sensor[4] > 600 && sensor[5] > 600  && sensor[6] > 600 && sensor[7] > 600) ) {
      cases = 4;
      break;
    }

    // Case5 için;
    else if (cases == 5 &&  (sensor[4] < 300 && sensor[5] < 300 && sensor[6] < 300) )  {
      cases = 5;
      break;
    }

    else if (cases == 6 &&  ((sensor[7] < 300 || sensor[0] < 300) && (sensor[3] < 300 || sensor[4] < 300)))  {
      cases = 6;
      break;
    }

    else if (cases == 7 && ((sensor[2] < 300 && sensor[3] < 300 && sensor[4] < 300) || (sensor[1] < 300 && sensor[2] < 300 && sensor[3] < 300)))  {
      cases = 7;
      break;
    }

    else if (cases == 8 && (sensor[0] < 300 && sensor[1] < 300 && sensor[2] < 300 && sensor[7] > 600))  {
      cases = 8;
      break;
    }

    else if (cases == 9 &&  (sensor[3] < 200 || sensor[4] < 200) && (sensor[1] < 200 || sensor[0] < 200))  {
      cases = 9;
      break;
    }


    else if (cases == 10 && (sensor[7] < 300 && sensor[6] < 300 && sensor[5] < 300 && sensor[4] < 300 && sensor[0] > 600))  {
      cases = 10;
      break;
    }

    else if (cases == 11 && (sensor[3] < 200 || sensor[4] < 200) && (sensor[1] < 200 || sensor[0] < 200))  {
      cases = 11;
      break;
    }

    else if (cases == 12 && (sensor[7] < 300 && sensor[6] < 300 && sensor[5] < 300 && sensor[4] < 300 && sensor[0] > 600))  {
      cases = 12;
      break;
    }

    else if (cases == 13 && (sensor[0] > 600 && sensor[1] > 600  && sensor[2] > 600 && sensor[3] > 600 && sensor[4] > 600 && sensor[5] > 600  && sensor[6] > 600 && sensor[7] > 600))  {
      cases = 13;
      break;
    }

  else if (cases == 14 && (sensor[7] < 300 && sensor[6] < 300 && sensor[5] < 300 && sensor[4] < 300 && sensor[0] > 600))  {
      cases = 14;
      break;
    }

     else if (cases == 15 && (sensor[0] > 600 && sensor[1] > 600  && sensor[2] > 600 && sensor[3] > 600 && sensor[4] > 600 && sensor[5] > 600  && sensor[6] > 600 && sensor[7] > 600) ) {
      cases = 15;
      break;
    }

      else if (cases == 16 && (sensor[3] < 200 || sensor[4] < 200) && (sensor[1] < 200 || sensor[0] < 200) ) {
      cases = 16;
      break;
    }

     else if (cases == 17 && (sensor[3] < 200 || sensor[4] < 200) && (sensor[7] < 200 || sensor[0] < 200) ) {
      cases = 17;
      break;
    }

     else if (cases == 18 && (sensor[3] < 200 || sensor[4] < 200) && (sensor[7] < 200 || sensor[0] < 200) ) {
      cases = 18;
      break;
    }

       else if (cases == 19 && (sensor[3] < 200 || sensor[4] < 200) && (sensor[7] < 200 || sensor[0] < 200) ) {
      cases = 19;
      break;
    }

    //Test
    else if (test == 1 ) {
      //MotorEncoderSpeed(2000,100,70);
      //MotorBrake(100);
      //test=0;
      //Calibration();
      //break;
      Pid();
      //MotorSpeed(-20,20);
    }
  }
  switch (cases) {
    case 0:
      Case0();
      cases = 1;
      break;
    case 1:
      Case1();
      cases = 2;
      break;
    case 2:
      Case2();
      cases = 3;
      break;
    case 3:
      Case3();
      cases = 4;
      break;
    case 4:
      Case4();
      cases = 5;
      break;
    case 5:
      Case5();
      cases = 6;
      break;
    case 6:
      Case6();
      cases = 7;
      break;
    case 7:
      Case7();
      cases = 8;
      break;
    case 8:
      Case8();
      cases = 9;
      break;
    case 9:
      Case9();
      cases = 10;
      break;
    case 10:
      Case10();
      cases = 11;
      break;
    case 11:
      Case11();
      cases = 12;
      break;
    case 12:
      Case12();
      cases = 13;
      break;
      case 13:
      Case13();
      cases = 14;
      break;
      case 14:
      Case14();
      cases = 15;
      break;
    case 15:
      Case15();
      cases = 16;
      break;
    case 16:
      Case16();
      cases = 17;
      break;
      case 17:
      Case17();
      cases = 18;
      break;
       case 18:
      Case18();
      cases = 19;
      break;
    case 19:
      Case19();
      cases = 20;
      break;
    
      


  }


}
