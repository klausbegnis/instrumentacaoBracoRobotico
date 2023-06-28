#include <Servo.h>

#define servo1 9 // Pino de controle do servo 1
#define servo2 10 // Pino de controle do servo 2
#define servo3 11 // Pino de controle do servo 3

Servo s1;
Servo s2;
Servo s3;

//se as coordenadas forem dadas em milímetros, basta converter essas declarações para milímetros

float L1 = 12; //altura até o primeiro palito na barra roscada em cm (Partindo da base do motor de passo)
float L2 = 12; //Comprimento do primeiro palito (distância da barra roscada até o primeiro servo)
float L3 = 12; //Comprimento do segundo palito (distância do primeiro servo - grande - até o segundo servo - pequeno)
float Le = 12; //Comprimento do último palito (distância do segundo servo - pequeno - até o sensor de distância)

//Posição que será adquirida pelo Rasp (aqui ta uma variável somente para validação)
float x = 5;
float y = 5;
float z = 5;

//Variáveis auxiliares para as contas
float r;
float h;
float alpha;
float beta;
float gama;

//ângulos dos servos adquiridos dos cálculos
float theta1 = 0; //Referente ao Servo1 - motor de passo (valor inicial configurável)
float theta2 = 0; //Referente ao Servo2 - motor servo grande (valor inicial configurável)
float theta3 = 0; //Referente ao Servo3 - motor servo pequeno (valor inicial configurável)

void setup() {
  Serial.begin(9600);
  
  s1.attach(servo1); //ASSOCIAÇÃO DO PINO DIGITAL AO OBJETO DO TIPO SERVO
  s1.write(theta1); //Também precisamos definir onde vai ser o 0 desses servos
  
  s2.attach(servo2); //ASSOCIAÇÃO DO PINO DIGITAL AO OBJETO DO TIPO SERVO
  s2.write(theta2); //Também precisamos definir onde vai ser o 0 desses servos
  
  s3.attach(servo3); //ASSOCIAÇÃO DO PINO DIGITAL AO OBJETO DO TIPO SERVO
  s3.write(theta3); //Também precisamos definir onde vai ser o 0 desses servos  

}

void loop() {
  theta1 = atan2(x, y)*180/PI;

  r = sqrt(pow(x,2) + pow((y-L2),2));
  h = sqrt(pow((L1-z),2) + pow(r,2));
  alpha = acos((pow(L3,2) + pow(Le,2) - pow(h,2))/(2*L3*Le))*180/PI;
  gama = acos((pow(L3,2) + pow(h,2) - pow(L3,2))/(2*L3*h))*180/PI;
  beta = atan2(r, L1-z)*180/PI;

  theta2 = 90 - gama - beta;
  theta3 = 180 - alpha;
  
  Serial.print(r); Serial.print("\t");
  Serial.print(beta); Serial.print("\t");
  Serial.print(gama); Serial.print(" 1\n");

  Serial.print(theta1); Serial.print("\t");
  Serial.print(theta2); Serial.print("\t");
  Serial.print(theta3); Serial.print(" 2\n");

  Serial.println();

  s1.write(theta1);
  s2.write(theta2);
  s3.write(theta3);

}
