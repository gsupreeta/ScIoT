#include <ArduinoMqttClient.h>
#include <WiFiNINA.h>


///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = "Swapnil@31";        // your network SSID (name)
char pass[] = "Swapnil@2103";     // your network password

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[] = "broker.hivemq.com";
int        port     = 1883;
const char topic2[]  = "HDU/Building1/Monitoring/PDDL";
const char topic[]  = "HDU/Building1/Monitoring/OverCrowd";
const char topic3[]  = "real_unique_topic_3";

//set interval for sending messages (milliseconds) 
const long interval = 8000;
unsigned long previousMillis = 0;


// ultrasonic sensor constants 
int currentPeople = 0;
int buzzer = 8;
int sensor1[] = {4,5};
int sensor2[] = {6,7};
int sensor1Initial;
int sensor2Initial;
String sequence = "";
int timeoutCounter = 0;
int maxPeople = 5; // maximum number of people allowed before the alarm goes off
char  message_read ;
int someInt;

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  // attempt to connect to Wifi network:
  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("You're connected to the network");
  Serial.println();

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();

  // set the message receive callback
  mqttClient.onMessage(onMqttMessage);

  

  // subscribe to a topic
  mqttClient.subscribe(topic);
  mqttClient.subscribe(topic2);
  mqttClient.subscribe(topic3);
  
  // topics can be unsubscribed using:
  // mqttClient.unsubscribe(topic);

//  Serial.print("Topic: ");
//  Serial.println(topic);
//  Serial.print("Topic: ");
//  Serial.println(topic2);
//  Serial.print("Topic: ");
//  Serial.println(topic3);

//  Serial.println();

  pinMode(buzzer, OUTPUT);
  pinMode(9, OUTPUT);
  delay(500);
  sensor1Initial = measureDistance(sensor1);
  sensor2Initial = measureDistance(sensor2);
}

void loop() {
  // call poll() regularly to allow the library to receive MQTT messages and
  // send MQTT keep alives which avoids being disconnected by the broker
char receivedData = Serial1.read();
  
  // call poll() regularly to allow the library to send MQTT keep alives which
  // avoids being disconnected by the broker
  mqttClient.poll();

 unsigned long currentMillis = millis();

 if (currentMillis - previousMillis >= interval) {
    // save the last time a message was sent
 previousMillis = currentMillis;

 
 int sensor1Val = measureDistance(sensor1);
 int sensor2Val = measureDistance(sensor2);


  
 //Process the data
if(sensor1Val < sensor1Initial - 30 && !(sequence.equals("1")))
{
 sequence += "1";
}
else if(sensor2Val < sensor2Initial - 30 && !(sequence.equals("2")))
{
    sequence += "2";
}


if(sequence.equals("12")){
  currentPeople++;  
  sequence="";
  delay(550);
 }
 
else if(sequence.equals("21") && currentPeople > 0)
{
  currentPeople--;  
  sequence="";
  delay(550);
}
  
if(sequence.equals("12"))
{
 currentPeople++;  
 sequence="";
 timeoutCounter=0;
 delay(550);
 }
 
 else if(sequence.equals("21") && currentPeople > 0)
 {
   currentPeople--;  
   sequence="";
   timeoutCounter=0;
   delay(550);
 }


  //Resets the sequence if it is invalid or timeouts
if(timeoutCounter > 10)
{
  sequence="";
  timeoutCounter=0;  
}
if (sequence.equals("1")|| sequence.equals("2") )
 {
   timeoutCounter++;
 }

Serial.print(" \n counter:");
Serial.println(currentPeople);
Serial.print(" \n sequence:");
Serial.print(sequence);
Serial.print(" \n");



  //If the number of people is too high, trigger the buzzer
if(currentPeople > 2)
{
   digitalWrite(8, HIGH);
   delay(1000);
// mqttClient.beginMessage(topic);
// mqttClient.print(" maximum people reached ");
// mqttClient.endMessage();  
}
else
{
  digitalWrite(8, LOW); 
}


   
//Serial.print("Sending message to topic: ");
//Serial.println(topic);
//Serial.println(currentPeople);

     //send message, the Print interface can be used to set the message contents
 mqttClient.beginMessage(topic);
 mqttClient.print(currentPeople);
 mqttClient.endMessage();
Serial.println();
 }
}


void onMqttMessage(int messageSize) {
  // we received a message, print out the topic and contents
  Serial.println("Received a message with topic '");
  Serial.print(mqttClient.messageTopic());
  Serial.print("', length ");
  Serial.print(messageSize);
  Serial.println(" bytes:");

  // use the Stream interface to print the contents
  int i=0;
  String temp;
  while (mqttClient.available()) {
    temp += (char)mqttClient.read();
  }
  if(!(temp=="0"))
  {
    if(temp=="8")
    {
      analogWrite(9,64);
    }
    if(temp=="9")
    {
      analogWrite(9,255);
    }
    if(temp=="7")
    {
      analogWrite(9,0);
    }
  }
}
//Returns the distance of the ultrasonic sensor that is passed in
//a[0] = echo, a[1] = trig
int measureDistance(int a[]) {
  pinMode(a[1], OUTPUT);
  digitalWrite(a[1], LOW);
  delayMicroseconds(2);
  digitalWrite(a[1], HIGH);
  delayMicroseconds(10);
  digitalWrite(a[1], LOW);
  pinMode(a[0], INPUT);
  long duration = pulseIn(a[0], HIGH, 100000);
  return duration / 29 / 2;
}
