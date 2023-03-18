#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/joystick.h>
#include <cstdio>
#include <geometry_msgs/Vector3.h>
#include <geometry_msgs/PoseStamped.h>
#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

#include "sensor_msgs/Joy.h"

// #include "header.h"

#define JOY_DEV "/dev/input/js0"

using namespace std;

int main(int argc, char **argv)
{
    //QCoreApplication a(argc, argv);

    ros::init(argc, argv, "footpedal");
    ros::NodeHandle n;
    int publish_rate;
    n.param(std::string("/publish_rate"), publish_rate, 100);
    ros::Publisher foot_pub;



    foot_pub = n.advertise<geometry_msgs::Vector3>("footPedal", 1);

	geometry_msgs::Vector3 Foot;
	Foot.x = 0;Foot.y = 0;Foot.z = 0;

    int joy_fd, *axis= NULL, num_of_axis = 0, num_of_buttons=0,x;
    char *button = NULL , name_of_joystick[80];
    struct js_event js;
    // input of joystick values to variable joy_fd
    if((joy_fd = open(JOY_DEV,O_RDONLY))== -1 )
    {
        cout<< " couldn't open the joystick \n " <<endl;

        return -1;
    }
    ioctl(joy_fd, JSIOCGAXES , &num_of_axis);
    ioctl(joy_fd, JSIOCGBUTTONS , &num_of_buttons);
    ioctl(joy_fd, JSIOCGNAME(80), &name_of_joystick);

        axis = (int *) calloc(num_of_axis , sizeof(int));
        button = (char *) calloc( num_of_buttons , sizeof (char));

    fcntl( joy_fd, F_SETFL , O_NONBLOCK ); // use non - blocking methods


    ros::Rate loop_rate(publish_rate);
    ros::AsyncSpinner spinner(2);
    spinner.start();
    while(ros::ok()) // infinite loop

    {
        // read the joystick
        read (joy_fd, &js , sizeof(struct js_event));

        // see what to do with the event
        switch(js.type & ~ JS_EVENT_INIT)
        {
            case JS_EVENT_AXIS :

                axis [ js.number ] = js.value;

            case JS_EVENT_BUTTON :

                button [js.number ] = js.value;
        }

        Foot.x = button[0];
        Foot.y = button[1];
        Foot.z = button[2];
        foot_pub.publish(Foot);

        loop_rate.sleep();
        fflush(stdout);


    }

    close(joy_fd);
return 0;
}

