#include <CMRI.h>

/**
 * C/MRI speedometer outputs
 * ======================================
 * 
 * 
 * 1: Set up a JMRI connection, see hello_world, steps 1-4
 * 2: Open Tools > Tables > Lights and click 'Add'
 * 3: Add a new light at hardware address 1, then click 'Create'.
 * 4: Repeat for hardware address 2, 3, 4 and close the window. Ignore the save message.
 * 5: Click on 'Sensors' and set up new sensors for hardware address 1, 2, 3 and 4.
 * 6: You'll notice the TX and RX LEDs burst into life. This is JMRI polling the state of our sensors.
 * 7: Ground pin 6, you'll see sensor #1 go Active, while the rest are Inactive.
 * 8: Switch to Lights and play around with the State buttons. Congratulations!
 * 
 * Debugging:
 * Open the CMRI > CMRI Monitor window to check what is getting sent and received.
 * With 'Show raw data' turned on the output looks like:
 *    [41 50]  Poll ua=0
 *    [41 52 01 00 00]  Receive ua=0 IB=1 0 0 
 * 
 * 0x41 = 65 = A = address 0
 * 0x50 = 80 = P = poll, i.e. PC asking C/MRI to transmit its state back to PC
 * 
 * 0x41 = 65 = A = address 0
 * 0x52 = 82 = R = receive, i.e. PC receiving state data from C/MRI 
 * 0x01 = 0b00000001 = 1st bit is high
 * 0x00 = 0b00000000 = all other bits off
 * 
 * Shift in chip(s) use pins 4-7 as control and data pins. 
 */

#include <Arduino.h>
#include <cmri.h>

#define NUMBER_OF_SHIFT_CHIPS 2
#define DATA_WIDTH NUMBER_OF_SHIFT_CHIPS * 8

int EnablePin = 4;  // CE  Lilac
int LoadPin = 5;    // SH/LD   white
int ClockPin = 6;   // CLK   green
int DataPin = 7;    // SER_OUT (Data bit) blue
int LogPin = 8;     // working LED indicator
int flag = HIGH;

CMRI cmri(0, DATA_WIDTH, 4);  // defaults to a SMINI with address 0. SMINI = 24 inputs, 48 outputs

void setup() {
  //Serial.begin(9600, SERIAL_8N2);  // make sure this matches your speed set in JMRI
  Serial.begin(115200);
  // init shift in chips
  pinMode(LoadPin, OUTPUT);
  pinMode(EnablePin, OUTPUT);
  pinMode(ClockPin, OUTPUT);
  pinMode(DataPin, INPUT);
  pinMode(LogPin, OUTPUT);

  digitalWrite(ClockPin, LOW);
  digitalWrite(LoadPin, HIGH);
}

void loop() {
  long bitVal;


  // get next command from JMRI.
  if (cmri.process()) {
    digitalWrite(LogPin, HIGH);
  } else {
    digitalWrite(LogPin, LOW);
  }


  // update shift data
  digitalWrite(EnablePin, HIGH);
  digitalWrite(LoadPin, LOW);
  delayMicroseconds(5);  // delay to let data in shift register stabilize
  digitalWrite(LoadPin, HIGH);
  digitalWrite(EnablePin, LOW);
  // shift registers now have updated pin data

  for (int i = 0; i < DATA_WIDTH; i++) {
    bitVal = digitalRead(DataPin);  // read next bit from register
    cmri.set_bit(i, bitVal);        // save bit as CMRI bit
    digitalWrite(ClockPin, HIGH);   // pop clock pin up and down to get next bit from register data
    delayMicroseconds(5);
    digitalWrite(ClockPin, LOW);
  }  // for
}  // loop
