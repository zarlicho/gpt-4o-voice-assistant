#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

LiquidCrystal_I2C lcd(0x27, 16, 2); // Inisialisasi alamat I2C (0x27) dan ukuran LCD 16x2

void setup() {
  Serial.begin(9600);
  while (!Serial); 
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
  lcd.init(); // Inisialisasi LCD
  lcd.backlight(); // Nyalakan backlight LCD
  pinMode(LED_BUILTIN, OUTPUT); // Set the built-in LED as an output

  Serial.println("Scan your RFID card or tag");
  lcd.setCursor(0, 0);
  lcd.print("Scan your RFID");
  lcd.setCursor(0, 1);
  lcd.print("card or tag");
}

void loop() {
  // Look for new cards
  if (!rfid.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Turn on the built-in LED when a card is scanned
  digitalWrite(LED_BUILTIN, HIGH);

  // Print the UID of the card on Serial Monitor
  Serial.print("Card UID: ");
  String uidString = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(rfid.uid.uidByte[i], HEX);
    uidString += String(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
    uidString += String(rfid.uid.uidByte[i], HEX);
  }
  Serial.println();

  // Display the UID on LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Card UID:");
  lcd.setCursor(0, 1);
  lcd.print(uidString);

  // Halt PICC
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();

  delay(5000); // Delay to allow reading and displaying

  // Turn off the built-in LED after displaying
  digitalWrite(LED_BUILTIN, LOW);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Scan your RFID");
  lcd.setCursor(0, 1);
  lcd.print("card or tag");
}
