#include <Arduino_HTS221.h>
#include <Arduino_APDS9960.h>

/*******************************************
*Declaration of global varibales
*******************************************/
float temp_sensed;
float humidity_sensed;
int gesture;

/*******************************************
 * Initializing and setting up sensors
 ********************************************/
void setup()
{ 
  pinMode(LED_BUILTIN, OUTPUT);     
  Serial.begin(9600);               

  HTS.begin();                                              

  if (!APDS.begin()) {                                       
    Serial.println("Error initializing gesture sensor!");    
  }
}

/******************************************
 * Sensing data and passing the same
 *******************************************/
void loop() {

//Gesture detection 
for (int i = 0; i < 1000; i++)
 {
    APDS.setGestureSensitivity(90);
    if(APDS.gestureAvailable()){ 
    gesture = APDS.readGesture();
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("Gesture:");
    Serial.println(gesture);
    }
    delay(10); 
 }

//Temperature monitoring
temp_sensed = HTS.readTemperature();
Serial.print("Temperature: ");
Serial.println(temp_sensed);

humidity_sensed = HTS.readHumidity();
Serial.print("Humidity: ");
Serial.println(humidity_sensed);

digitalWrite(LED_BUILTIN, LOW);
}
