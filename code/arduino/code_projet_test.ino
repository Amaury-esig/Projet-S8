
#include <Servo.h> 
 #include <Wire.h>

#define SLAVE_ADDRESS 0x03
int dataReceived = 0;
int commande;
int flag=0;
int temps = 1500; //censé être à mi-chemin entre 1000 et 2000, un bon point de départ
int vitesse = 1500;
Servo monServo;
Servo moteur;
/*
 const char DOUT_TRIGGER_1 = 7;
const char DIN_ECHO_1 = 6;
 const char DOUT_TRIGGER_2 = 4;
const char DIN_ECHO_2 = 5;


 const char DOUT_TRIGGER_3 = 13;
const char DIN_ECHO_3 = 10;
float distance_1;
float distance_3;
float distance_2;
*/

void setup()
{
    Serial.begin(9600);
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
   // Wire.onRequest(sendData);
    //Serial.println("Hello World");
  /*  pinMode(DOUT_TRIGGER_1, OUTPUT);
    pinMode(DIN_ECHO_1, INPUT);
    pinMode(DOUT_TRIGGER_2, OUTPUT);
    pinMode(DIN_ECHO_2, INPUT);
    pinMode(DOUT_TRIGGER_3, OUTPUT);
    pinMode(DIN_ECHO_3, INPUT);*/
    monServo.attach(11);
    moteur.attach(9);
    //on démarre à une valeur censé être la moitié de
    //l'excursion totale de l'angle réalisé par le servomoteur
    monServo.writeMicroseconds(temps);
    moteur.writeMicroseconds(vitesse);
     delay(1000);
}
 
void loop()
{

}






////*********************foncton pour la mesure de distance

/*
float dist_1(){
 digitalWrite(DOUT_TRIGGER_1, LOW);
    delayMicroseconds(2);
    digitalWrite(DOUT_TRIGGER_1, HIGH);
    delayMicroseconds(10);
    digitalWrite(DOUT_TRIGGER_1, LOW);
    
    distance_1= pulseIn(DIN_ECHO_1, HIGH) / 58.0;
    return distance_1;
  }

float dist_2(){
 digitalWrite(DOUT_TRIGGER_2, LOW);
    delayMicroseconds(2);
    digitalWrite(DOUT_TRIGGER_2, HIGH);
    delayMicroseconds(10);
    digitalWrite(DOUT_TRIGGER_2, LOW);
    
    distance_2= pulseIn(DIN_ECHO_2, HIGH) / 58.0;
    return distance_2;
  }
  float dist_3(){
 digitalWrite(DOUT_TRIGGER_3, LOW);
    delayMicroseconds(2);
    digitalWrite(DOUT_TRIGGER_3, HIGH);
    delayMicroseconds(10);
    digitalWrite(DOUT_TRIGGER_3, LOW);
    
    distance_3= pulseIn(DIN_ECHO_3, HIGH) / 58.0;
    return distance_3;
  }


*/



  //*********************foncton reception des commande de la raspberry PI par I2C



  void receiveData(int byteCount){
    while(Wire.available()) {
        commande = Wire.read();
flag =1;
    }
  

  
        
        //on modifie la consigne si c'est un caractère qui nous intéresse
        if(commande == 1){
          
        vitesse = 1586;
        //vitesse = 100;
        }
       else if(commande == 2){
          
        vitesse = 1500;
        //vitesse = 90;
        }
       else{

          if(commande < 79 || commande > 102){
            vitesse = 1587;
            //vitesse = 110;
          }
          else {
          vitesse = 1585;
          //vitesse = 100;
          }
        temps = commande;
        
       }








        monServo.write(temps);
        //if( (dist_1()>50.0) and (dist_2()>25.0) and (dist_3()>25.0)   ){
        moteur.writeMicroseconds(vitesse);
        //}
        //else{
        
        //moteur.writeMicroseconds(1500);
     //   Serial.println("\nobstacle present, arret du moteur");
        //}

    
}
