# poolmonitoring
Raspberry pi Pool monitoring project

This is the phase 2 of my project which started with my spa monitoring (https://hackaday.io/project/10759-outdoor-hot-tub-monitoring)

This project is about monitoring a pool using a raspberry pi and a bunch of small sensors. Every sensor are hooked to a plastic mesh. When I had my pool dug in the ground, I asked to install a barel in the ground connected with a pipe to the pool. The barel is in the shed where all the mechanics of the pool is located. I'll put the mesh in the barel and it'll have access to the pool water without having to be in the actual pool (plus that will give me a place to fill the water using the float sensors and a solenoid for sprinkler).

The probing is done through arduino/raspberry pi, and sent to thingspeak for graphs. we will use ifft later to create alerts. Both arduino and raspberry pi are plugged together using usb cable. 

2 temperature sensors (DS18b20) waterproof. Connected using a 5k resistor (google how to connect to raspberry pi, fairly easy)

2 float sensor. simple foam sensor with a magnet, closing a circuit based on whether there's water or not. place one above another, will help knwoing water level in the pool and determine if we should open a valve to refill the pool.

1 ph sensor

1 ORP sensor

connecting the raspberry pi (2) with the arduino and the sensors is done with the following diagram (excuse the poor quality, i don't know which sofware to use).

<img src="https://github.com/mathieuduperre/poolmonitoring/raw/master/poolmonitoring.png">

<img src="https://github.com/mathieuduperre/poolmonitoring/raw/master/20170502_144557.jpg">

<img src="https://github.com/mathieuduperre/poolmonitoring/raw/master/20170502_144538.jpg">

<img src="https://github.com/mathieuduperre/poolmonitoring/raw/master/20170502_144541.jpg">

<img src="https://github.com/mathieuduperre/poolmonitoring/raw/master/20170502_144547.jpg">
