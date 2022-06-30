#include "OneWire.h"
#include "DallasTemperature.h"
 
OneWire oneWire(A1);
DallasTemperature ds(&oneWire);

void setup() {
  Serial.begin(9600);  // définition de l'ouverture du port série
  ds.begin();          // sonde activée
}

void loop() {
  ds.requestTemperatures();
  int t = ds.getTempCByIndex(0);
 
  Serial.print(t);
  Serial.println( "C");
 
  delay(500);
}
