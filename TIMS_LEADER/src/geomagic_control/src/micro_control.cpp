#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/timeb.h>
#include <stdint.h>
#include <stdbool.h>
#include "/home/leen/Ros_Files/myomni/src/geomagic_control/include/geomagic_control/libum.h"

typedef struct params_s
{
    float x, y, z, d, X, Y, Z, D, pressure_kpa, speed;
    int verbose, update, loop, dev, timeout, value, dim_leds, group;
    int calibrate_pressure, pressure_channel, valve_channel, reset_fluid_detector, pressure_sensor;
    bool lens_position, read_fluid_detectors;
    char *address;
} params_struct;

int main(int argc, char *argv[])
{
    um_state *handle = NULL;
    params_struct params;
    if((handle = um_open(params.address, params.timeout, params.group)) == NULL)
    {
        // Feeding NULL handle is intentional, it obtains the
        // last OS error which prevented the port to be opened
        fprintf(stderr, "Open failed - %s\n", um_last_errorstr(handle));
        exit(1);
    }

    return 0;
}



