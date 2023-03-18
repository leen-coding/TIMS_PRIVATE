#include <ros.h>
// #include <geometry_msgs/Vector3.h>
#include <std_msgs/Bool.h>

const int row[8] = {
  2, 4, 6, 8, 10, 12, 14, 16
};
int timer = 1000;
// 2-dimensional array of column pin numbers:
const int col[8] = {
  3, 5, 7, 9, 11, 13, 15, 17
};

ros::NodeHandle nh;

bool tactile_info;

void messageCb( const std_msgs::Bool& msg){
  
  tactile_info = msg.data;

  if (tactile_info){
      digitalWrite(22, LOW);
      digitalWrite(23, LOW);

      for (int thisPin = 0; thisPin < 8; thisPin++) {
      
      digitalWrite(col[thisPin], LOW);
      digitalWrite(row[thisPin], LOW);
      
    }
    // delay(timer); 
  }
  else{
      digitalWrite(22, HIGH);
      digitalWrite(23, HIGH);
      for (int thisPin = 0; thisPin < 8; thisPin++) {
    
      digitalWrite(col[thisPin], HIGH);
      digitalWrite(row[thisPin], HIGH);
    }

  }
}

ros::Subscriber<std_msgs::Bool> sub("/Geomagic/tactileInfo", &messageCb );

void setup()
{

  for (int thisPin = 0; thisPin < 8; thisPin++) {
  // initialize the output pins:
    pinMode(col[thisPin], OUTPUT);
    pinMode(row[thisPin], OUTPUT);
    digitalWrite(col[thisPin], HIGH);
    digitalWrite(row[thisPin], HIGH); 
    
  }

  pinMode(22, OUTPUT);
  digitalWrite(22, HIGH);
  pinMode(23, OUTPUT);
  digitalWrite(23, HIGH);
  nh.initNode();
  nh.subscribe(sub);
}

void loop()
{
  
  nh.spinOnce();
  delay(1);
}