// Opdracht 8a - Nina Schrauwen
// This program receives and executes the commands given via the Pi
// Define constant variables
const int LED1 = 4;
const int LED2 = 7;

// Led setup and setup of seral communication
void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);  
  pinMode(LED2, OUTPUT);  
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
}

//  Main loop to translate and execute the commands received from the pi
void loop() {
  // If a serial connection has been established with the Pi
  if (Serial.available()) {
    Serial.println("Connected with pi");
    //  Read the command
    char cmd = Serial.read();
    // Command to turn on LED1, turn LED2 off (blinking sequence)
    if (cmd == 'A') {
      Serial.println("First sequence");
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, LOW);
      // Command to turn on LED2, turn LED1 off (blinking sequence)
    } else if (cmd == 'B') {
      Serial.println("Second sequence"); 
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, HIGH);
    }
  }
}
