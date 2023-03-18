#!/bin/bash
source ~/anaconda3/bin/activate TIMS
which python
source ./devel/setup.bash

roslaunch geomagic_control geomagic_headless.launch


