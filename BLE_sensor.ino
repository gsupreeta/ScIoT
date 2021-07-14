#include <Arduino_HTS221.h>
#include <Arduino_APDS9960.h>

float temp_sensed;
float humidity_sensed;
int gesture;

void setup()
{ 
  Serial.begin(9600);               // initialize serial communication at 9600 bits per second:
  Serial1.begin(9600);            // initialize UART with baud rate of 9600

  HTS.begin();                                              //Activate Temperature Sensor

  if (!APDS.begin()) {                                       //Gesture sensor checking
    Serial1.println("Error initializing gesture sensor!");    
  }
}


void loop() {

//Gesture detection 
for (int i = 0; i < 1000; i++)
 {
    APDS.setGestureSensitivity(90);
    if(APDS.gestureAvailable()){ 
    gesture = APDS.readGesture();
    Serial1.println(gesture);
    }
    delay(10);
 }

//Temperature monitoring
temp_sensed = HTS.readTemperature();
//Serial.print("Temperature:");
Serial.println(temp_sensed);
Serial1.println(temp_sensed);

humidity_sensed = HTS.readHumidity();
//Serial.print("Humidity:");
Serial.println(humidity_sensed);
Serial1.println(humidity_sensed);
}
