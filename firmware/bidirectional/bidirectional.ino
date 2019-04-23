#include "DueTimer.h"
#include "GPIO.h"

#define LENGTH 64 // we can change arduino hardware limit

GPIO<BOARD::D4> pin4out;
GPIO<BOARD::D7> pin7in;
volatile int i;
volatile int j;
enum sender_state {INIT, SENDING, RECEIVING} state;
volatile int handler_running = 0;
volatile char sendBinaryNum[LENGTH][8];
char receiveBinaryNum[LENGTH][8];
DueTimer myTimer = DueTimer(0);

void setup() {
  // put your setup code here, to run once:
  //myTimer.attachInterrupt(handler).setPeriod(125);
  pin7in.input();
  pin4out.output();
  pinMode(DAC0, OUTPUT);
  analogWrite(DAC0, 24);

  Serial.begin(14400);
  Serial1.begin(14400);
  while (!Serial);
  
  pin4out = 1;
  while (!pin7in);
  while (Serial.available()) Serial.read();
  //Serial.print("Setup Complete");
}

void loop() {

  if(Serial.available()) {

    Serial1.write(Serial.read());
    
  }

  else if(Serial1.available()) {

    Serial.write(Serial1.read());
    
  }
  
}

/* void loop() {
  char strArray[64];
  
  while(pin7in){
	  if(Serial.available()){
		
		delay(10);
		  
		for(int i = 0; i<64; i++){
		  strArray[i] = Serial.read();
		}
		
		printbincharpad(strArray);
		myTimer.start();
		handler_running = 1;
		state = INIT;

		while(handler_running) delay(1);
		
	  } 
  }
  
  i = 0;
  j = 0;
  //for (int i = 0; i < 4000; i++);
  myTimer.start();
  handler_running = 1;
  state = RECEIVING;
  
  

  while(handler_running) delay(1);

  for(int k = 0; k < 64; k++) {
    strArray[k] = convertToChar(receiveBinaryNum[k]);
  }

  for(int k = 0; k < 64; k++) {
    Serial.print(strArray[k]);
  }
  
}

void handler() {
  switch (state) {
    case INIT:
      pin4out = 0;
      i = 0;
      j = 0;
      state = SENDING;
      break;
    case SENDING:
      pin4out = sendBinaryNum[i][j];
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
  case RECEIVING:
    receiveBinaryNum[i][j] = pin7in;
    if(j<7) {
        j++;
      } 
    else if (i<63){
        j=0;
        i++;
      }
    else {
        myTimer.stop();
        handler_running = 0;
		state = INIT;
      }
    break;
  }  
}



char convertToChar(char* binaryChar) {
  int multiplier = 0;
  int temp;
  int sum = 0;
  for(temp = 7; temp>=0; temp--) 
  sum += (binaryChar[temp]*(1 << multiplier++));
  return sum;
}

void printbincharpad(char * c) {
  for(int i = 0; i <= LENGTH; i++){
    for (int j = 7; j >= 0; --j)
    {
        sendBinaryNum[i][7-j] = (c[i] & (1 << j)) ? '1' : '0';
    }
  }
}*/
