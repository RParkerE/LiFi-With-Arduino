#include "DueTimer.h"
#include "GPIO.h"

#define LENGTH 64 // we can change arduino hardware limit

GPIO<BOARD::D4> pin4out;
enum sender_state {INIT, SENDING} state = INIT;
volatile int handler_running = 0;
volatile char binaryNum[LENGTH][8];
DueTimer myTimer = DueTimer(0);

void setup() {
  // put your setup code here, to run once:
  myTimer.attachInterrupt(handler).setPeriod(10);
  pin4out.output();

  Serial.begin(115200);
  while (!Serial);

  pin4out = 1;
}

void loop() {
  // put your main code here, to run repeatedly:
  // digitalWrite(4,state);
  //pin4out = state;
  char strArray[64];
  
  while(!Serial.available());

  while(Serial.available()){
    //delay(50);

    for(int i = 0; i<64; i++){
      strArray[i] = Serial.read();
    }
  }

  printbincharpad(strArray);
  myTimer.start();
  handler_running = 1;

  while(handler_running) delay(1);
}

void handler() {  
  static int i;
  static int j;
  switch (state) {
    case INIT:
      pin4out = 0;
      i = 0;
      j = 0;
      state = SENDING;
      break;
    case SENDING:
      pin4out = binaryNum[i][j];
      if(j<7) {
        j++;
      } else if (i<63){
        j=0;
        i++;
      } else {
        pin4out = 1;
        myTimer.stop();
        state = INIT;
        handler_running = 0;
      }
      break;
  }
}

void printbincharpad(char * c)
{
  for(int i = 0; i <= LENGTH; i++){
    for (int j = 7; j >= 0; --j)
    {
        binaryNum[i][7-j] = (c[i] & (1 << j)) ? '1' : '0';
    }
  }
}
