#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  150 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  600 // this is the 'maximum' pulse length count (out of 4096)
uint8_t servonum = 0;

const int eyepin = 11;
const int servopin = 10;
const int earpin = 9;
const int M1pin = 6;
const int Dir1pin = 8;
const int M2pin = 5;
const int Dir2pin = 7;
const int limitpin1 = 12;
const int limitpin2 = 13;
// variables will change:
int buttonState1 = 0;         // variable for reading the pushbutton status
int buttonState2 = 0; 
int Dir1 = LOW;
int Dir2 = LOW;
int M1 = 0;
int M2 = 0;
int eye = 0;
int servo = 0;
int ear = 0;

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

      // variables to hold the parsed data

int integerFromPC = 0;


boolean newData = false;
boolean beaconmode = true;
boolean connectedmode = false

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//========================================
void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part 
    eye = atoi(strtokIndx); // copy it to eye
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    ear = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    M1 = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    Dir1 = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    M2 = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    Dir2 = atoi(strtokIndx);     // convert this part to an integer

    if (Dir1==0){
      Dir1=LOW;
    }    else{
      Dir1=HIGH;}
    if (Dir2==0){
      Dir2=LOW;
    }
    else{
      Dir2=HIGH;}
    if (eye>=255){
      eye=255;}
    else if (eye<=0){
      eye=0;}
    if (servo>=100){
      servo=100;}
    else if (servo<=0){
      servo=0;}
    if (ear>=255){
      ear=255;}
    else if (ear<=0){
      ear=0;}
    if (M1>=255){
      M1=255;}
    else if (M1<=0){
      M1=0;}
    if (M2>=255){
      M2=255;}
    else if (M2<=0){
      M2=0;}
   

    }

//============

void showParsedData() {
    Serial.print("eye  ");
    Serial.println(eye);
    Serial.print("servo  ");
    Serial.println(servo);
    Serial.print("ear  ");
    Serial.println(ear);
    Serial.print("M1  ");
    Serial.println(M1);
    Serial.print("Dir1  ");
    Serial.println(Dir1);
    Serial.print("M2  ");
    Serial.println(M2);
    Serial.print("Dir2  ");
    Serial.println(Dir2);
    
}
//==================================================
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(1000);
  
  pinMode(eyepin, OUTPUT);
  pinMode(servopin, OUTPUT);
  pinMode(earpin, OUTPUT);
  pinMode(M1pin, OUTPUT);
  pinMode(Dir1pin, OUTPUT);
  pinMode(M2pin, OUTPUT);
  pinMode(Dir2pin, OUTPUT);
  pinMode(limitpin1, INPUT);
  pinMode(limitpin2, INPUT);

  analogWrite(eyepin,eye);
  analogWrite(servopin,servo);
  analogWrite(earpin,ear);
  analogWrite(M1pin,M1);
  analogWrite(M2pin,M2);
  digitalWrite(Dir1pin,Dir1);
  digitalWrite(Dir2pin,Dir2);
  }

void loop() {
  // put your main code here, to run repeatedly:
if (beaconmode) {
     delay(1000);
     Serial.write('*');
      rc=Serial.read();
     // Serial.read() and check for "I_hear_you"
     if (rc=='p') {
       beaconmode = false;
       delay(50)
       Serial.write('k');
       delay(50)
       Serial.write('k');
       delay(50)
       Serial.write('k');
       delay(50)
       Serial.write('k');
       delay(50)
       Serial.write('k');
       delay(50)
       Serial.write('k');
       // now the two devices are "connected"
       connectedmode = true;
   }
if (connectedmode) {
  recvWithStartEndMarkers();
    if (newData == true) {
      strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
      parseData();
      newData = false;
    }
 eyestalkmotor();
 rotationmotor();
 iris();
 eyelight();
 earlight();
         
     // do normal stuff
   }
}
      
recvWithStartEndMarkers();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
    parseData();
    newData = false;
    }
 eyestalkmotor();
 rotationmotor();
 iris();
 eyelight();
 earlight();
}
//========================================

//=============================================
void eyestalkmotor() {
   // read the state of the pushbutton value:
  buttonState1 = digitalRead(limitpin1);
  buttonState2 = digitalRead(limitpin2);
  Dir2 = Dir2;
  M2 = M2;
  if (buttonState1==HIGH && Dir2==HIGH){
  M2=0;
  // do Thing A
}
  else if (buttonState2==HIGH && Dir2==LOW)
{
  M2=0;
    // do Thing B
}
  else if (buttonState2==HIGH && buttonState1==HIGH)
{
  M2=0;
    // do Thing B
}
  else 
{
  Dir2=Dir2;
  // do Thing C
}

analogWrite(M2pin,M2);
digitalWrite(Dir2pin,Dir2);  
}
//===============================================
void rotationmotor() {
  Dir1 = Dir1;
  M1 = M1;
analogWrite(M1pin,M1);
digitalWrite(Dir1pin,Dir1);  
}
//==================================================
void iris() {
  pulselength = map(servo, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(0, 0, pulselength)

}
//============================================
void eyelight() {
  eye = eye;
analogWrite(eyepin,eye);

}
//==========================================
void earlight() {
  ear = ear;
analogWrite(earpin,ear);

}
