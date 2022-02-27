# Doorbot

## Goal:
I would like to access a website and press a button to control a servo motor wirelessly. It will be controlled by an Espressif ESP32.

## Layout

There is an esp32 folder with files that will be uploaded onto the board, an a web folder for files that will eventually run on a server in an external VM. There is a `/esp32/wifi.txt` file that contains the wifi log-in details that must be loaded into the ESP32 SPIFFS file system.

More details on the webapp are in `web/README.md`. The Flask server will send an HTTP request to the ESP32 when someone presses the "buzz" button.


Some original code from: https://github.com/madhephaestus/ESP32Servo/blob/master/examples/Knob/Knob.ino

## Some helpful commands

Finds PID of processes: `sudo lsof -n | grep "UART"`
