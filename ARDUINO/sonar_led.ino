#include <Servo.h>

// I/O DEFINITIONS

//#define LED 52
#define ECHO 51
#define TRIG 50
#define X_READ A0
#define Y_READ A1
// step motor values
#define ora 8
#define bro 9
#define yel 10
#define red 11
// BUTTONS
#define BR 42
#define BL 43
#define BSTP 21
#define BST 45
// SERVO PINS
#define servo2 A8 // Pino de controle do servo 2
#define servo3 A7 // Pino de controle do servo 3

Servo s2;
Servo s3;

// SERVO MOTOR'S VARIABLES

float L1 = 135; //altura até o primeiro palito na barra roscada em cm (Partindo da base do motor de passo)
float L2 = 95; //Comprimento do primeiro palito (distância da barra roscada até o primeiro servo)
float L3 = 105; //Comprimento do segundo palito (distância do primeiro servo - grande - até o segundo servo - pequeno)
float Le = 130; //Comprimento do último palito (distância do segundo servo - pequeno - até o sensor de distância)

float r;
float h;
float alpha;
float beta;
float gama;
float z = 10;// mm objective height

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
    float degreePerStep = 5;

    void moveToPosition(float theta)
    {
      if (theta > 0)
      {
        while (current_position < theta)
        {
          //Serial.println(current_position);
          walkOneStepRight();
          current_position += degreePerStep;
          if (not(current_position + degreePerStep >= theta))
          {
             for (int i = 0; i < 4; i+=1)
            {
                digitalWrite(startPin+i,0);
                //continue;
            }
            if (currentStep == RY)
            {
                currentStep = OB;
            }
            else {
                currentStep = currentStep*0b0010;
            }
          }
        }
      }
      else 
      {
        while (current_position > theta)
        {
          //Serial.println(current_position);
          walkOneStepLeft();
          current_position -= degreePerStep;
          if (not(current_position - degreePerStep <= theta))
          {
            for (int i = 0; i < 4; i+=1)
            {
                digitalWrite(startPin+i,0);
                //continue;
            }
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
        //Serial.println();
    }
    void walkOneStepLeft()
    {
        for (int i = 0; i < 4; i++)
        {
            digitalWrite(startPin+i,(1 <= (currentStep & (1 << i))));
            //Serial.print((1 <= (currentStep & (1 << i))));
        }
        delay(50);
        //Serial.println();
    }

     void setupOrigin()
    {
      /*
      int setup_theta =0;
      
      while (true)
      {
        Serial.print("Current pos: ");
        Serial.println(current_position);
        Serial.print("Setup theta: ");
        Serial.println(setup_theta);
        
        if(digitalRead(BR) > 0)
        {
          setup_theta ++;
          //walkOneStepLeft();
        }
        if(digitalRead(BL) > 0)
        {
          setup_theta --;
          //walkOneStepRight();
        }
        //delay(100);
        moveToPosition(setup_theta);
        if (digitalRead(BST) == 1)
        {
          current_position = 0;
          break;
        }
      }*/
        moveToPosition(50);
        delay(50);
        moveToPosition(-50);
        delay(50);
        moveToPosition(50);
        delay(50);
        moveToPosition(0);       
        current_position = 0;
        
        while (digitalRead(BST) !=1)
        {
          delay(50);
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
  pinMode(BR,INPUT);
  pinMode(BL,INPUT);
  pinMode(BST,INPUT);
  pinMode(LED_BUILTIN,OUTPUT);
  attachInterrupt(digitalPinToInterrupt(BSTP),stop,RISING);
  s2.attach(servo2); //ASSOCIAÇÃO DO PINO DIGITAL AO OBJETO DO TIPO SERVO
  s2.write(90); //Também precisamos definir onde vai ser o 0 desses servos
  s3.attach(servo3); //ASSOCIAÇÃO DO PINO DIGITAL AO OBJETO DO TIPO SERVO
  s3.write(0); //Também precisamos definir onde vai ser o 0 desses servos
  STEP_MOTOR.setupOrigin();
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
  
  x_pulse = pulseIn(Y_READ,HIGH);
  y_pulse = pulseIn(X_READ,HIGH);
  x_reading = x_pulse*X_MAX/PERIOD_MAX/1000;
  y_reading = y_pulse*Y_MAX/PERIOD_MAX/1000;

  //Serial.print("Coordenada X: ");
  //Serial.println(x_reading); 
  //Serial.print("Coordenada Y: ");
  //Serial.println(y_reading);

  REAL_COORDINATE = convert2Reference(x_reading,y_reading);

  Serial.print("Converted X: ");
  Serial.print(REAL_COORDINATE.x);
  Serial.print("Converterd Y: ");
  Serial.print(REAL_COORDINATE.y);
  
  go2objective(REAL_COORDINATE);
  //STEP_MOTOR.moveToPosition(50);
  //delay(100);
  //STEP_MOTOR.moveToPosition(-50);
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
  gama = acos((pow(L3,2) + pow(h,2) - pow(Le,2))/(2*L3*h))*180/PI;
  beta = atan2(r, L1-z)*180/PI;

  theta2 = 90 - gama - beta; // elbow angle
  Serial.print("theta2: ");
  Serial.println(theta2);
  theta3 = alpha; // wrist angle
  Serial.print("theta3: ");
  Serial.println(theta3);
  s2.write(theta2);
  s3.write(theta3);
  STEP_MOTOR.moveToPosition(theta1);
  delay(5000);
  s2.write(90);
  s3.write(0);
  STEP_MOTOR.moveToPosition(-theta1);
  while (digitalRead(BST)!=1)
  {
    delay(500);
  }
}

void stop()
{
  digitalWrite(LED_BUILTIN,HIGH);
  while(digitalRead(BST) != 0)
  {
    delay(250);
  }
  digitalWrite(LED_BUILTIN,LOW);
}