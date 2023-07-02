#include <Servo.h>

// I/O DEFINITIONS

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

// BUTTONS
#define BR 42
#define BL 43
#define BSTP 44
#define BST 45

// LEDS
#define GREEN 39
#define YELLOW 40
#define RED 41

// SERVO PINS
#define servo2 A8 // Pino de controle do servo 2
#define servo3 A9 // Pino de controle do servo 3

Servo s2;
Servo s3;

// SERVO MOTOR'S VARIABLES

float L1 = 120; //altura até o primeiro palito na barra roscada em cm (Partindo da base do motor de passo)
float L2 = 120; //Comprimento do primeiro palito (distância da barra roscada até o primeiro servo)
float L3 = 120; //Comprimento do segundo palito (distância do primeiro servo - grande - até o segundo servo - pequeno)
float Le = 120; //Comprimento do último palito (distância do segundo servo - pequeno - até o sensor de distância)

float r;
float h;
float alpha;
float beta;
float gama;
float z = 5; // mm objective height

float theta1 = 0; //Referente ao StepMotor - motor de passo (valor inicial configurável)
float theta2 = 0; //Referente ao Servo2 - motor servo grande (valor inicial configurável)
float theta3 = 0; //Referente ao Servo3 - motor servo pequeno (valor inicial configurável)

// STEP MOTOR VARIABLES

int OB = 0b0001;
int BO = 0b0010;
int YR = 0b0100;
int RY = 0b1000;

// CONVERSION VARIABLES

float X_MAX = 196;
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

// struct's definitions

struct coordinate
{
  double x;
  double y;
};

struct stepMotor
{
    int startPin = ora;
    int currentStep = OB;
    int current_position=0;
    float degreePerStep = 1;

    void moveToPosition(float theta)
    {
      if (theta > 0)
      {
        while (current_position < theta)
        {
          Serial.println(current_position);
          walkOneStepRight();
          current_position += degreePerStep;
          if (not(current_position + degreePerStep >= theta))
          {
            if (currentStep == RY)
            {
                currentStep = OB;
            }
            else {
                currentStep = currentStep*0b0010;
            }
            for (int i = 0; i < 4; i+=1)
            {
              digitalWrite(startPin+i,0);
              continue;
            }
          }
        }
      }
      else 
      {
        while (current_position > theta)
        {
          walkOneStepLeft();
          current_position -= degreePerStep;
          if (not(current_position - degreePerStep <= theta))
          {
            if (currentStep == OB)
            {
                currentStep = RY;
            }
            else {
                currentStep = currentStep/0b0010;
            }
          }
        }
      }
    }

    void walkOneStepRight()
    {
        for (int i = 0; i < 4; i+=1)
        {
            digitalWrite(startPin+i,(1 <= (currentStep & (1 << i))));
            //Serial.print((1 <= (currentStep & (1 << i))));
        }
        delay(50);
    }
    void walkOneStepLeft()
    {
        for (int i = 0; i < 4; i++)
        {
            digitalWrite(startPin+i,(1 <= (currentStep & (1 << i))));
        }
        delay(50);
    }

    void setupOrigin()
    {
      int setup_theta =0;
      while (true)
      {
        if(digitalRead(BR) > 0)
        {
          setup_theta ++;
        }
        if(digitalRead(BL) > 0)
        {
          setup_theta --;
        }
        delay(100);
        moveToPosition(setup_theta);

        if (digitalRead(BSTP) > 0)
        {
          current_position = 0;
          break;
        }
      }
      
    }

};

// struct initialization
stepMotor STEP_MOTOR;
coordinate REAL_COORDINATE; 

void setup() {
  Serial.begin(57600);
  pinMode(ECHO,INPUT);
  pinMode(TRIG,OUTPUT);
  pinMode(X_READ,INPUT);
  pinMode(Y_READ,INPUT);
  pinMode(red,OUTPUT);
  pinMode(yel,OUTPUT);
  pinMode(ora,OUTPUT);
  pinMode(bro,OUTPUT);
  s2.attach(servo2); //ASSOCIAÇÃO DO PINO DIGITAL AO OBJETO DO TIPO SERVO
  s2.write(theta2); //Também precisamos definir onde vai ser o 0 desses servos
  s3.attach(servo3); //ASSOCIAÇÃO DO PINO DIGITAL AO OBJETO DO TIPO SERVO
  s3.write(theta3); //Também precisamos definir onde vai ser o 0 desses servos
}

void loop() {
  // put your main code here, to run repeatedly:
  //distance = readDistance(); //mm
  //Serial.println(distance);
  /*
  if (distance < 150){
    //setLedAndWait(0, HIGH,false);
    Serial.print("Distancia: ");
    Serial.println(distance);
  }
  
  else{
    //setLedAndWait(0, LOW,false);
  }*/
  /*
  x_pulse = pulseIn(Y_READ,HIGH);
  y_pulse = pulseIn(X_READ,HIGH);
  x_reading = x_pulse*X_MAX/PERIOD_MAX/1000;
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
  
  //go2objective(REAL_COORDINATE);*/
  STEP_MOTOR.moveToPosition(50);
  delay(10);
  STEP_MOTOR.moveToPosition(-50);
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

void go2objective(coordinate COORD)
{
  float x = COORD.x;
  float y = COORD.y;

  theta1 = atan2(x, y)*180/PI; // step motor angle

  r = sqrt(pow(x,2) + pow((y-L2),2));
  h = sqrt(pow((L1-z),2) + pow(r,2));
  alpha = acos((pow(L3,2) + pow(Le,2) - pow(h,2))/(2*L3*Le))*180/PI;
  gama = acos((pow(L3,2) + pow(h,2) - pow(L3,2))/(2*L3*h))*180/PI;
  beta = atan2(r, L1-z)*180/PI;

  theta2 = 90 - gama - beta; // elbow angle
  theta3 = 180 - alpha; // wrist angle

  s2.write(theta2);
  s3.write(theta3);
  STEP_MOTOR.moveToPosition(theta1);
}