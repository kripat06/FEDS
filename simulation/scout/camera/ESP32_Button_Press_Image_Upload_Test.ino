
#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include "SD_MMC.h"
#include "esp_camera.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Replace with your network credentials
const char* ssid = "********************";
const char* password = "********************";

#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
 
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define BUTTON_PIN 4
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
uint8_t _buffer[10000];
const int ledPin =  5;    // the number of the LED pin

int pingState = 0;
bool piPing = false;
bool takePic = false;
int location = 0;
String printLocalTime(){
  time_t rawtime;
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    ESP.restart();
  }
  char timeStringBuff[50]; //50 chars should be enough
  strftime(timeStringBuff, sizeof(timeStringBuff), "%d_%Y_%H:%M:%S", &timeinfo);
  //print like "const char*"
  Serial.println(timeStringBuff);

  //Optional: Construct String object 
  String asString(timeStringBuff);
  return asString;
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  // Initialize Wi-Fi
  pinMode(ledPin, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  display.clearDisplay();
  delay(100);
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(0,0);
  display.print("Connecting to Wifi");
  display.startscrollright(0x00, 0x02);
  display.display();
  delay(100);
  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  display.stopscroll();
  display.clearDisplay();
  display.setCursor(0,0);
  display.setTextSize(2);
  display.print("Connected to Wifi");
  display.display();
  delay(500);
  display.clearDisplay();
  display.display();

  Serial.println(WiFi.localIP());
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 16500000;
  config.pixel_format = PIXFORMAT_JPEG;
  //init with high specs to pre-allocate larger buffers
  config.frame_size = FRAMESIZE_VGA;
  config.jpeg_quality = 10;
  config.fb_count = 1;
  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
  const char* ntpServer = "pool.ntp.org";
  const long  gmtOffset_sec = 14400;
  const int   daylightOffset_sec = 3600;
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

void loop() {
  piPing  = checkForPing();
  if (piPing == true) {
    takePic = true;
    digitalWrite(ledPin, HIGH);
    location = location + 1;
    String locationString = String(location);
  } else {
    // turn LED off
    digitalWrite(ledPin, LOW);
  }
  if(piPing){
    WiFiClientSecure *client = new WiFiClientSecure;
    String timeinfo = printLocalTime();
    camera_fb_t * fb = NULL;
    display.setTextColor(WHITE);
    display.setTextSize(1);
    display.setCursor(0,0);
    display.print("TAKING PICTURE.....");
    display.startscrollright(0x00, 0x02);
    display.display();
    delay(300);
    fb = esp_camera_fb_get();
    int fileindex = 0;
    int filelen = fb->len;
    if(client) {
      // set secure client with certificate
      client->setInsecure();
      //create an HTTPClient instance
      HTTPClient https;
      
      //Initializing an HTTPS communication using the secure client
      Serial.print("[HTTPS] begin...\n");
      if (https.begin(*client, "https://y********************.amazonaws.com/dev-feds-upload-api/upload/" + String(location))) {  // HTTPS
        https.addHeader("Content-Type", "application/octet-stream");
        https.addHeader("x-api-key", "****************************************);
        display.clearDisplay();
        delay(100);
        display.setCursor(0,0);
        display.setTextSize(1);
        display.print("[HTTPS] POST...");
        display.display();
        delay(500);
        Serial.print("[HTTPS] POST...\n");
        display.clearDisplay();
        display.display();
        delay(100);
        // start connection and send HTTP header
        for (int i = 0; i < 10000; i++) {
          if (filelen) {
            _buffer[i] = fb->buf[fileindex];
          }
          else {
            _buffer[i] = 0;
          }
          fileindex++;
          filelen--;
        }
        int httpCode = https.POST(_buffer, 10000);
        // httpCode will be negative on error
        if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
         Serial.printf("[HTTPS] GET... code: %d\n", httpCode);
        // file found at server
          if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
            // print server response payload
            String payload = https.getString();
            Serial.println(payload);
            display.clearDisplay();
            delay(100);
            display.setCursor(0,0);
            display.setTextSize(1);
            display.print("success");
            display.display();
            delay(500);
            display.clearDisplay();
            display.display();
            delay(100);
          } 
        }
        else {
          Serial.printf("[HTTPS] GET... failed, error: %s\n", https.errorToString(httpCode).c_str());
          display.clearDisplay();
          display.setCursor(0,0);
          display.setTextSize(1);
          display.print("[HTTPS] GET... failed");
          display.display();
          delay(500);
          display.clearDisplay();
          display.display();
          delay(100);
        }
        https.end();
      }
    }
    else {
      Serial.printf("[HTTPS] Unable to connect\n");
      display.clearDisplay();
      display.setCursor(0,0);
      display.setTextSize(1);
      display.print("[HTTPS] Unable to connect");
      display.display();
      delay(500);
      display.clearDisplay();
      display.display();
      delay(100);
    }
    esp_camera_fb_return(fb);
    takePic = false;
  }

}

bool checkForPing() {
  bool takePicture = false;
  int buttonState = digitalRead(BUTTON_PIN);
  if (buttonState == HIGH) {
    takePicture = true;
  } else {
    // turn LED off
    takePicture = false;
  }
  return takePicture;
}
