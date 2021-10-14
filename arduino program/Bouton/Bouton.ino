int etatCapteur;
int t1;
int t2;
int tvit1;
int tvit2;
int revs = 0;
int i;
float vitesse;

void setup() 
{
  pinMode(2, INPUT_PULLUP);
  Serial.begin(9600);
  t1 = millis();
  tvit1 = millis();
  i=0;
}

void loop() 
{
  etatCapteur = digitalRead(2);
  //Serial.println(etatCapteur);
  while (etatCapteur==LOW) {
    if (i==0) {
      revs += 1;
      tvit2 = millis();
      vitesse = (2.1/((tvit2-tvit1)*0.001))*3.6;
      tvit1 = tvit2;
    }
    delay(50);
    etatCapteur = digitalRead(2);
    //Serial.println("#2");
    i=1;  
  }
  i=0;

  t2 = millis();

  if ((t2-t1)>500) {
    Serial.println(String(revs)+";"+String(vitesse));
    revs=0;
    t1 = t2;
    //Serial.println("#3");
  }
}
