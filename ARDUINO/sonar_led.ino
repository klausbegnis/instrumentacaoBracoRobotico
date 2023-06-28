//#define LED 52
#define ECHO 51
#define TRIG 50
#define X_READ A0
#define Y_READ A1
// step motor values
#define ora 46
#define bro 47
#define yel 48
#define red 49
//10,10,10,10
//lm,av,ml,va
//RYBO
int OB = 0b0001;
int BO = 0b0010;
int YR = 0b0100;
int RY = 0b1000;

float X_MAX = 190;
float Y_MAX = 160;
float PERIOD_MAX = 100;
float PERIOD_MIN = 0;

float y_offset = 150;

double x_pulse;
double y_pulse;
double x_reading;
double y_reading;
double distance;
double realCoordinates;

struct coordinate
{
  double x;
  double y;
};

struct stepMotor
{
    int startPin = ora;
    int currentStep = OB;

    void sendStepConfig()
    {
        for (int i = 0; i < 4; i+=1)
        {
            digitalWrite(startPin+i,(1 <= (currentStep & (1 << i))));
        }
        delay(50);
        for (int i = 0; i < 4; i+=1)
        {
            digitalWrite(startPin+i,0);
        }
        if (currentStep == RY)
        {
            currentStep = OB;
        }
        else {
            currentStep = currentStep*0b0010;

        }

    }

};

stepMotor STEP_MOTOR;
coordinate REAL_COORDINATE; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  pinMode(ECHO,INPUT);
  pinMode(TRIG,OUTPUT);
  //pinMode(LED,OUTPUT);
  pinMode(X_READ,INPUT);
  pinMode(Y_READ,INPUT);
  pinMode(red,OUTPUT);
  pinMode(yel,OUTPUT);
  pinMode(ora,OUTPUT);
  pinMode(bro,OUTPUT);

  STEP_MOTOR.sendStepConfig();
}

void loop() {
  // put your main code here, to run repeatedly:
  distance = readDistance(); //mm
  Serial.println(distance);
  /*
  if (distance < 150){
    //setLedAndWait(0, HIGH,false);
    Serial.print("Distancia: ");
    Serial.println(distance);
  }
  
  else{
    //setLedAndWait(0, LOW,false);
  }*/
  
  x_pulse = pulseIn(X_READ,HIGH);
  y_pulse = pulseIn(Y_READ,HIGH);

  // max time to pulse DC=100 -> T=0.01 -> 10ms
  // (10ms-0) / 100 = 0.1
  x_reading = x_pulse*X_MAX/PERIOD_MAX/1000; // trocar para *?
  y_reading = y_pulse*Y_MAX/PERIOD_MAX/1000;

  Serial.print("Coordenada X: ");
  Serial.println(x_reading);

  
  Serial.print("Coordenada Y: ");
  Serial.println(y_reading);

  REAL_COORDINATE = convert2Reference(x_reading,y_reading);

  Serial.print("Converted X: ");
  Serial.print(REAL_COORDINATE.x);

  Serial.print("Converterd Y: ");
  Serial.print(REAL_COORDINATE.y);


  STEP_MOTOR.sendStepConfig();
}

void setLedAndWait(int ts, bool setter,bool wait){
  //digitalWrite(LED,setter);
  if (wait){delay(ts);};
}

double readDistance()
{
// pulso de envio
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  
  // tempo em 1 do echo
  unsigned long duracao = pulseIn(ECHO, HIGH);
  
  return duracao;
}

coordinate convert2Reference(double x, double y)
{
  coordinate RESULT;
  double x_converted;
  double y_converted = y + y_offset; // add the distance from the base
  // to the detection area
  
  //centers the step motor
  if ((x > (X_MAX/2)) or (x < (X_MAX/2)))
  {
    x_converted = x - (X_MAX/2);
  }
  else
  {
    x_converted = 0;
  } 
  RESULT.x = x_converted;
  RESULT.y = y_converted;
  return RESULT;
}