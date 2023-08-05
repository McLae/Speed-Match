#define NUMBER_OF_SHIFT_CHIPS   1
#define DATA_WIDTH   NUMBER_OF_SHIFT_CHIPS * 8


int EnablePin  = 4; // CE  brownj
int LoadPin    = 5; // SH/LD   white
int ClockPin   = 6; // CLK   green
int DataPin    = 7; // SER_OUT (Data bit) blue


unsigned long pinValues;
unsigned long oldPinValues;

long bitValArray[DATA_WIDTH];
bool valueChanged;

void setup()
{
  Serial.begin(9600);

  pinMode(LoadPin, OUTPUT);
  pinMode(EnablePin, OUTPUT);
  pinMode(ClockPin, OUTPUT);
  pinMode(DataPin, INPUT);

  digitalWrite(ClockPin, LOW);
  digitalWrite(LoadPin, HIGH);

  pinValues = read_shift_regs();
  print_byte();
  oldPinValues = pinValues;
}

void loop()
{
  pinValues = read_shift_regs();

  if (pinValues != oldPinValues)
  {
    print_byte();
    oldPinValues = pinValues;
  }

}

unsigned long read_shift_regs()
{
  long bitVal;
  unsigned long bytesVal = 0;

  digitalWrite(EnablePin, HIGH);
  digitalWrite(LoadPin, LOW);
  delayMicroseconds(5);
  digitalWrite(LoadPin, HIGH);
  digitalWrite(EnablePin, LOW);

  for (int i = 0; i < DATA_WIDTH; i++)
  {
    bitVal = digitalRead(DataPin);
    bitValArray[i] = bitVal;

    bytesVal |= (bitVal << ((DATA_WIDTH - 1) - i));

    digitalWrite(ClockPin, HIGH);
    delayMicroseconds(5);
    digitalWrite(ClockPin, LOW);
  }

  return (bytesVal);
}

void print_byte() {
  byte i;

  Serial.println("*Shift Register Values:*\r\n");

  for (byte i = 0; i < DATA_WIDTH ; i++)
  {
    Serial.print("P");
    Serial.print(i + 1);
    Serial.print(" ");
    Serial.print(bitValArray[i]);
    Serial.print(" ");

  }
  Serial.println();
  for (byte i = 0; i < DATA_WIDTH; i++)
  {
    Serial.print(pinValues >> i & 1, BIN);

    if (i > 8) {
      Serial.print(" ");
    }
    Serial.print("  ");

  }

  Serial.print("\n");
  Serial.println(); Serial.println();

}
