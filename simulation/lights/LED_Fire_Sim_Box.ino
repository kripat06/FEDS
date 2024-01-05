#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#include "avr/interrupt.h";

#define PIN 1
#define NUMPIXEL 1   //how many pixel on the strip.
#define DETECT 2
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXEL, PIN, NEO_GRB + NEO_KHZ800);

int MinBrightness = 20;       //value 0-255
int MaxBrightness = 50;      //value 0-255

int numLoops1 = 10;
int numLoops2 = 10;
int numLoops3 = 10;
int numLoops4 = 10;          //add new integer and value for more color's loop if needed.

int fadeInWait = 4;          //lighting up speed, steps.
int fadeOutWait = 4;         //dimming speed, steps.

bool lightPower = true;
int detected;
//---------------------------------------------------------------------------------------------------//

void setup() {
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
  #endif
  GIMSK = 0b00100000;    // turns on pin change interrupts
  PCMSK = 0b00010011;    // turn on interrupts on pins PB0, PB1, &amp;amp; PB4
  sei();                 // enables interrupts
  pinMode(DETECT, INPUT);//define detect input pin
  strip.begin();
  strip.show();
}

/*
rgbBreathe(strip.Color(insert r,g,b color code),numLoops(refer to integer above), (duration for lights to hold before dimming. insert 0 to skip hold)
rainbowBreathe(numLoops(refer to integer above),(duration for lights to hold before dimming. insert 0 to skip hold)
*/

void loop() {
    detected = digitalRead(DETECT); // read Laser sensor
    if(detected == LOW){
      rgbBreathe(strip.Color(0, 255, 0), numLoops1, 0); //red.
    }
    else if (detected == HIGH) {      
      rgbBreathe(strip.Color(255, 0, 0), numLoops1, 0); //red.
      rgbBreathe(strip.Color(255, 20, 0), numLoops3, 0); //red.
      rgbBreathe(strip.Color(255, 40, 0), numLoops3, 0); //red.
      rgbBreathe(strip.Color(255, 50, 0), numLoops3, 0); //red.
      rgbBreathe(strip.Color(255, 30, 0), numLoops3, 0); //red.
      rgbBreathe(strip.Color(226, 60, 0), numLoops2, 0); //red.
      rgbBreathe(strip.Color(255, 70, 0), numLoops3, 0); //red.
      rgbBreathe(strip.Color(255, 84, 0), numLoops4, 0); //red.
      rgbBreathe(strip.Color(255, 84, 0), numLoops4, 0); //red.
      rgbBreathe(strip.Color(255, 64, 0), numLoops4, 0); //red.
      rgbBreathe(strip.Color(255, 74, 0), numLoops4, 0); //red.
      rgbBreathe(strip.Color(255, 54, 0), numLoops4, 0); //red.
      rgbBreathe(strip.Color(255, 24, 0), numLoops4, 0); //red.
      rgbBreathe(strip.Color(255, 34, 0), numLoops4, 0); //red.
    }
}

ISR(PCINT0_vect)
{
  detected = digitalRead(DETECT);
  if( digitalRead(DETECT) == LOW) {
   rgbBreathe(strip.Color(0, 0, 0), numLoops4, 0); //red.
   delay(10000);
 }
}


//Functions -----------------------------------------------------------------------------------------//
void rgbBreathe(uint32_t c, uint8_t x, uint8_t y) {
  
  for (int j = 0; j < x; j++) {
    for (uint8_t b = MinBrightness; b < MaxBrightness; b++) {
      strip.setBrightness(b * 255 / 255);
      for (uint16_t i = 0; i < strip.numPixels(); i++) {
        strip.setPixelColor(i, c);
      }
      strip.show();
      delay(fadeInWait);
    }
    strip.setBrightness(MaxBrightness * 255 / 255);
    for (uint16_t i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.show();
      delay(y);
    }
    for (uint8_t b = MaxBrightness; b > MinBrightness; b--) {
      strip.setBrightness(b * 255 / 255);
      for (uint16_t i = 0; i < strip.numPixels(); i++) {
        strip.setPixelColor(i, c);
      }
      strip.show();
      delay(fadeOutWait);
    }
  }
}

void rainbowBreathe(uint8_t x, uint8_t y) {
  for (int j = 0; j < x; j++) {
    for (uint8_t b = MinBrightness; b < MaxBrightness; b++) {
      strip.setBrightness(b * 255 / 255);
      for (uint8_t i = 0; i < strip.numPixels(); i++) {
        strip.setPixelColor(i, Wheel(i * 256 / strip.numPixels()));
      }
      strip.show();
      delay(fadeInWait);
    }
    strip.setBrightness(MaxBrightness * 255 / 255);
    for (uint8_t i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(i * 256 / strip.numPixels()));
      strip.show();
      delay(y);
    }
    for (uint8_t b = MaxBrightness; b > MinBrightness; b--) {
      strip.setBrightness(b * 255 / 255);
      for (uint8_t i = 0; i < strip.numPixels(); i++) {
        strip.setPixelColor(i, Wheel(i * 256 / strip.numPixels()));
      }
      strip.show();
      delay(fadeOutWait);
    }
  }
}


//NeoPixel Wheel for Rainbow---------------------------------------

uint32_t Wheel(byte WheelPos) {
  WheelPos = 140 - WheelPos;       //the value here means - for 255 the strip will starts with red, 127-red will be in the middle, 0 - strip ends with red.
  if (WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if (WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}
