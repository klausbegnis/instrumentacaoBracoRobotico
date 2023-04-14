#define LED 52
#define ECHO 51
#define TRIG 50
double distance;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  pinMode(ECHO,INPUT);
  pinMode(TRIG,OUTPUT);
  pinMode(LED,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  distance = readDistance(); //mm
  //if (distance < 30)
  //{
  // setLedAndWait(HIGH,10);
  //};
  //setLedAndWait(HIGH,1000);
  Serial.print(distance);
  Serial.print("Teste \n");

  if (distance < 150){
    setLedAndWait(0, HIGH,false);
  }
  else{
    setLedAndWait(0, LOW,false);
  }

  //setLedAndWait(100,HIGH);
  //setLedAndWait(100,LOW);
}

void setLedAndWait(int ts, bool setter,bool wait){
  digitalWrite(LED,setter);
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