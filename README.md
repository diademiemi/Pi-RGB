# Raspberry Pi RGB LED Controller

This program is to control RGB LEDs connected to the Raspberry Pi GPIO pins. It uses the GPIOZero library to interface with the pins.  
This program is made of two parts, one daemon process which you run on the Raspberry Pi, and a controller script, which sends data to the Pi over a UDP socket. This could also run on localhost, to run only on the Pi. The default UDP port is 5807, and it runs on 127.0.0.1 by default.  

I am creating this for the LED strip I wired to a Raspberry Pi following this guide: https://dordnung.de/raspberrypi-ledstrip/  
However, it should work with any LED which has a pin for red, green and blue, you can customize the GPIO pins in the .env file.  

## USAGE

### Basic usage

Install all required pip packages  
`pip3 install -r requirements.txt`  

Start the daemon script. If you want to communicate with it over network, change `LISTEN_ADDRESS` in `.env` or pass `-a x.x.x.x` with an address.  
`./daemon.py`  
Listening on all addresses:  
`./daemon.py -a 0.0.0.0`  
If you do not want the process to run in the background, add `-f`, this will also print every input it receives from the controller script, and any errors.  

You can now interface with this daemon with the `controller.py` script. By default it will attempt to communicate to 127.0.0.1, you will have to change `CONNECT_ADDRESS` in `.env` or pass `-a x.x.x.x`. In all options, command arguments are given precedent over the `.env` file.  
`./controller.py -c red`  
Connect to an address:  
`./controller.py -c 192.168.2.241`  


### Setting colours

There are 4 types of colour settings: single, strobe, fade and breathe.  

To set a single static colour, pass `-c` followed by a colour name as defined by [W4C](https://www.w3.org/TR/css-color-3/#svg-color) or a 6-digit hex code. To use a hex code, prefix it with #, this will likely require you to escape the argument in quotes as this character will get ignored in most shells.  
`./controller.py -c green`  
`./controller.py -c '#00ff00`  

The other 3 types support multiple comma-seperated colours.  

The strobe effect will jump between the given colours in order, without an animation.  
`./controller.py -s red,green,blue`  
For all the animated sequences, you can supply `-t` to set the time between colours, you can also set the default in `.env`, if neither of these are found, it will default to 1.0, one second.  
`./controller.py -s red,green,blue -t 2.5`  

The fade effect will smoothly transition between the colours in order, and on the last one it will loop back to the first one.  
`./controller.py -f black,purple,white,yellow`  

The breathe effect will fade from black, to the colours while fading to black in between. Black is counted as a colour, so by default, every specified colour will take 2 seconds, instead of the usual 1.  
`./controller.py -b aqua,deeppink,white,deeppink`  

### Presets

You can define presets in a YAML file, by default `presets.yaml`, mandatory options are colours and type, the time option will default to 1.
This is an example definition for a preset. It would be the same as executing `./controller.py -b aqua,deeppink,white,deeppink -t 1`  
```
trans:
  colours:
    - aqua
    - deeppink
    - white
    - deeppink
  type: breathe
  time: 1
```

To use this, supply the `-P` argument to the command followed by the preset name.  
`./controller.py -P trans`  
If your YAML file is not in the default location, supply `-F /path/to/file.yaml` to override it.  
`./controller.py -F /path/to/presets.yaml -P trans`  
