# rc-pi-car
Python code to control remotely a Raspberry PI car using Playstation 4 controller connected to a PC and receieve the video from a camera located in the car to a browser

# Description:

This code is to control remotely a Raspberry PI car with a PS4 controller connected to a PC. The PS4 Controller will be connected to a PC using USB cable. If you have a Raspberry PI camera, the video is sent to the PC and can be viewed in a web browser. No driver or special installation is required on the PC nor the Raspberry PI. 
The code is tested in PC with linux and MacOS, but it should work in Windows with minimal adjustments. 
No bluetooh is used. 

# Installation instructions on the PC  

Download the code in your pc:

git clone https://github.com/rubencardenes/rc-pi-car.git

# Installation instructions on the Raspberry PI:

Download the code in your Raspberry PI:

git clone https://github.com/rubencardenes/rc-pi-car.git

The following instructions are required to setup a http video stream on the Raspberry PI and be able to see that in any browser on your PC:

First, make sure you enable the camera on the PI: 
`sudo raspi-config`
Select: Interfacing options
Enable Camera 

Now install the h264-live-player from 131 user:  

```
git clone git@github.com:131/h264-live-player.git player
cd player
npm install
```

# Running the script 

Suppose, the IP of your Raspberry PI is 192.168.1.20 

Run the scripts in exactly this order:

In the Raspberry PI:
`python controller_server_on_pi.py`

In your PC:
`python controller_client.py 192.168.1.20`

Now in your PC open a web page:

http://192.168.1.20:8080


## Credits

User 131 on GitHub for the h264-live-player
Clay L. McLeod  <clay.l.mcleod@gmail.com> for the PS4 controller class 
http://www.elektronx.de/motoren-mit-ps4-controller-steuern/ for the control callbacks
Youtube sentdex channel for great explanation on sockets: https://www.youtube.com/watch?v=Lbfe3-v7yE0&t=238s



