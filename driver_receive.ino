#include "DueTimer.h"
#include "GPIO.h"

#define LENGTH 64 // we can change arduino hardware limit

GPIO<BOARD::D7> pin7in;
volatile int handler_running = 0;
char binaryNum[LENGTH][8];

volatile int i;
volatile int j;

DueTimer myTimer = DueTimer(0);

void setup() {
  // put your setup code here, to run once:
  myTimer.attachInterrupt(handler).setPeriod(10);
  pin7in.input();

  Serial.begin(115200);
  while (!Serial);
}

void loop() {
  // put your main code here, to run repeatedly:
  char strArray[64];
  
  while(pin7in);

  i = 0;
  j = 0;
  myTimer.start();
  handler_running = 1;

  while(handler_running) delay(1);

  for(int k = 0; k < 64; k++) {
    strArray[k] = convertToChar(binaryNum[k]);
  }

  for(int k = 0; k < 64; k++) {
    Serial.print(strArray[k]);
  }
}

void handler() {  
  binaryNum[i][j] = pin7in;
  if(j<7) {
    j++;
  } else if (i<63){
    j=0;
    i++;
  } else {
    pin7in = 1;
    myTimer.stop();
    handler_running = 0;
  }
}

char convertToChar(char* binaryChar)
{
  int multiplier = 0;
  int temp;
  int sum = 0;
  for(temp = 7; temp>=0; temp--) 
  sum += (binaryChar[temp]*(1 << multiplier++));
  return sum;
}
