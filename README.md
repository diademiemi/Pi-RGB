# Raspberry Pi RGB LED Controller

This program is to control RGB LEDs connected to the Raspberry Pi GPIO pins. It uses the GPIOZero library to interface with the pins.  
This program is made of two parts, one daemon process which you run on the Raspberry Pi, and a controller script, which sends data to the Pi over a UDP socket. This could also run on localhost, to run only on the Pi. The default UDP port is 5807, and it runs on 127.0.0.1 by default.  

I am creating this for the LED strip I wired to a Raspberry Pi following this guide: https://dordnung.de/raspberrypi-ledstrip/  
However, it should work with any LED which has a pin for red, green and blue, you can customize the GPIO pins in the .env file.  

# TO IMPLEMENT
* CSS Colours  
* Automatic detection for CSS colours or hex  
* Multi colour patterns: breathe, strobe, fade  
* file to define presets  
