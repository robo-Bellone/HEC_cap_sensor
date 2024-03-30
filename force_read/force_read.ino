int SensorPin0 = A0; //analog pin 0
int SensorPin1 = A1; //analog pin 1
int SensorPin2 = A2; //analog pin 2
int SensorPin3 = A3; //analog pin 3
 
int HI_limit = 1000;
int LOW_limit = 0;
 
void setup(){
  
  Serial.begin(9600);
}
 
void loop(){
  int SensorReading0 = analogRead(SensorPin0); 
  int SensorReading1 = analogRead(SensorPin1); 
  int SensorReading2 = analogRead(SensorPin2); 
  int SensorReading3 = analogRead(SensorPin3); 
 
  int A0 = map(SensorReading0, LOW_limit, 1024, 0, HI_limit);
  int A1 = map(SensorReading1, LOW_limit, 1024, 0, HI_limit);
  int A2 = map(SensorReading2, LOW_limit, 1024, 0, HI_limit);
  int A3 = map(SensorReading3, LOW_limit, 1024, 0, HI_limit);
 
  Serial.print(A0);
  Serial.print(",");
  //Serial.print('\n');
  Serial.print(A1);
  Serial.print(",");
  Serial.print(A2);
  Serial.print(",");
  Serial.println(A3);
 
  delay(10); 
}
