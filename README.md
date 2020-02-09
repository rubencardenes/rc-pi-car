# rc-pi-car
Python code to control remotely a Raspberry PI car using Playstation 4 controller connected to a PC and receieve the video from a camera located in the car to a browser

# Description:

This code is to control remotely a Raspberry PI car with a PS4 controller connected to a PC. The PS4 Controller will be connected to a PC using USB cable. If you have a Raspberry PI camera, the video is sent to the PC and can be viewed in a web browser. No driver or special installation is required on the PC nor the Raspberry PI. 
The code is tested in PC with linux and MacOS, but it should work in Windows with minimal adjustments. 
No bluetooh is used. 

# Features

- Remote control using PS4 Dualshock controller 
- Wifi video streaming using http server 
- Acceleration control using PS4 
- Control test script on localhost  

# Installation on the PC  

Download the code in your pc:

```
mkdir ~/PycharmProjects
cd ~/PycharmProjects
git clone https://github.com/rubencardenes/rc-pi-car.git
```

# Installation on the Raspberry PI:

1. Download the code in your Raspberry PI:

```
mkdir ~/PycharmProjects
cd ~/PycharmProjects
git clone https://github.com/rubencardenes/rc-pi-car.git
```

2. Install the h264-live-player streaming server  
This is required to setup a http video stream on the Raspberry PI. Then, you will be able to see that in any browser on your PC:

First, make sure you enable the camera on the PI: 
`sudo raspi-config`
Select: Interfacing options
Enable Camera 

Now install the h264-live-player from 131 user:  

```
cd ~/PycharmProjects
git clone git@github.com:131/h264-live-player.git player
cd player
npm install
```

Note that the installation is done in a folder that I call 'PycharmProjects'. Of course, you can change that folder to any other one. If you do so, remember to change line 51 in the script "controller_server_on_pi.py" to point to the right location of the js file: "server-pi.js"

# Running the script 

Suppose, the IP of your Raspberry PI is 192.168.1.20 

Run the scripts in exactly this order:

1. In the Raspberry PI:

```
cd ~/PycharmProjects/rc-pi-car
python controller_server_on_pi.py`
```

2. In your PC:

```
cd ~/PycharmProjects/rc-pi-car 
python controller_client.py 192.168.1.20
```

3. Open the video streaming. In your PC just open a web page with this address:

http://192.168.1.20:8080

Enjoy driving!

## Notes

My initial idea was to use the integrated bluetooth on the PI to control the car with the PS4. It didn't worked quite well. I managed to connect the PS4 controller device and sned the right commands to the PI. There are however three problems with this approack: 
- First one is that when I turned on wifi and bluetooh simultaneously in the PI, they interfere severely and makes the wifi connection to fail miserably, so there is no chance to receive a decent video signal from the camera. Sometimes I wasn't able to connect the PI via ssh or took more than a minute. Ridiculous.    
- Second: connection of the controller with bluetooh is a bit cumbersome and you have to start it manually every time on both sides, plus I found it not very stable. 
- Third: the range of bluetooh is not going to be as good as that provided by wifi.

Therefore, my solution here is to simply connect the PS4 controller to my computer using a USB cable, and send the PS4 controller signal from my computer to the PI, while at the same time receive video to my computer in the web browser. All is done by wifi and delay is negligible. It allows me to sit with my PC and run the car whenever I have wifi coverage (if the car does#t get stuck in any place). It works just great. 

I had some issues with the power supply. The Raspberry PI needs 5 V power supply than can be provided by the L298N H-bridge. However, I notice that if I use a set of 6 cheap AAA batteries, it wasnt enough to power the PI, so I added three more. I will change that to a Lipo battery or to better batteries. 
To save battery life, when I was testing the setup, I simply connected the PI using a micro USB power cable, which can be combined with the batteries with no problem. 

## Credits

- User 131 on GitHub for the h264-live-player: https://github.com/131/h264-live-player
- Clay L. McLeod  <clay.l.mcleod@gmail.com> for the PS4 controller class 
- Elektronx http://www.elektronx.de/motoren-mit-ps4-controller-steuern/ for the control callbacks
- Youtube sentdex channel for great explanation on sockets: https://www.youtube.com/watch?v=Lbfe3-v7yE0&t=238s
- The hardware part is mostly described in this great series of youtube videos by Daniel Murray: https://www.youtube.com/watch?v=icpZU_Pufno (The software part from that series differs greatly froom this software) 






