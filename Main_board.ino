#define LED_BUILTIN 25

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);      // set LED pin as output
  digitalWrite(LED_BUILTIN, LOW);    // switch off LED pin

  Serial1.begin(9600);            // initialize UART with baud rate of 9600
}

void loop() // run over and over
{
  while (Serial1.available() >= 0) {
    char receivedData = Serial1.read();   // read one byte from serial buffer and save to receivedData
    if (isDigit(receivedData)) {
      digitalWrite(LED_BUILTIN, HIGH);    // switch LED On
      delay(500);
    }
    else
    {
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
    }
  }
}
