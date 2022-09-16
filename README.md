# Wifi-controlled Stoplight

This lab's main focus is learning how to use GPIO pins by creating a mini stoplight on a raspberry pi and breadboard.  It connects to a remote webpage via wifi in order to not only create a circuit, but to create the user interface that controls it as well.  The result of this is an embedded system seeing as it is created and used for a specific purpose.  This report will deliver the schematics, setup, challenges, and results from this process.

## Requirements

* Use a Raspberry Pi and it’s GPIO pins
* Use a breadboard, LEDs (red, green, yellow), and resistors to create the circuit
* Connect to a webpage via wifi to control the stoplight remotely
* When one of the lights on webpage is pressed, the corresponding LED on the breadboard lights up
* When the cycle button on webpage is pressed, the LEDs rotate which one is lit (red, yellow, green, and back to red)
* Reasonable time interval for each LED in the cycle is used
* When the off button on webpage is pressed, any illuminated LED or current cycle mode is stopped and the machine is in the off state

## State Machine

The state machine (Figure 1)  is a visual representation of the states of the stoplight and the input needed to take it from one state to another.  We start in the “start” state and once started, it moves into the off position, regardless of any input.  From the off state, it can move into any other state, and back to off, depending on the input.  For example, if the machine is in the off state and the input 17 is given, the state will change to be in the “red” state.  This will continue for theoretically forever as there is no end unless power is removed.

![IMG_114BCFD1C6C3-1](https://user-images.githubusercontent.com/59840208/190528417-1aa93eae-7b30-4975-9a46-f528f8c0bae3.jpeg)
Figure 1

## System View
The user facing interface for this system is a html, css, and python webpage with a traffic light interface that the user can interact with (figure 2).  This interface includes an image of a stoplight with three coloured buttons corresponding with the lights on a traffic light, an “Off” button, and a “Cycle” button.  

When the user presses one of the lights on the traffic light image, the corresponding colour will show up on the connected LEDs through the raspberry pi’s GPIO pins, to the breadboard.  When the “Off” button is pressed, any light that was previously set to on, is set to an off state. When the “Cycle” button is pressed, the lights will, starting at red, cycle through the different lights at 2 second intervals.  If the “Off” button is pressed in this mode, the cycle will stop.

<img width="518" alt="Screen Shot 2022-09-15 at 5 58 13 PM" src="https://user-images.githubusercontent.com/59840208/190528586-fc80a6b8-f1b3-4ea5-8266-03eab7d99078.png">
Figure 2

## Component View
There are three main components to this lab.  The first is the computer and web browser from which the pi is connected to in order to control the circuit (more details mentioned in the System View section).  

The second is a raspberry pi.  This is what runs the server for the user interface and allows the code created to compile.  It also acts as the “power source” for the LED’s on the breadboard (technically the power source originates from the outlet that the raspberry pi is plugged into). This raspberry pi contains a microSD card with a version of Raspbian OS from 2018 so that the GPIO pins can be configured correctly.  The GPIO pins are the important part of this lab as they are what we use to interface our webpage with the pi and the breadboard.  This lab uses pins 17, 27, and 22, although different pins can be used.  This raspberry pi is also connected to a power source, the internet, and a keyboard and mouse, although after initial setup, the majority of programming done will be done remotely through a different computer with ssh.  

The third component is the breadboard.  This is what is implementing the circuits (Figure 4), allowing power to flow through to the LED’s to light them up when requested.  Figure 3 clearly shows the different parts of the breadboard circuits.  The first thing to note is the ground wire.  This wire provides power from the raspberry pi to the breadboard.  The next part of this component  is the other three cords connecting from the pi to the breadboard.  These are hooked up to pins 17, 27, and 22.  They are providing the electrical input to the board and the specific pins will allow for the programming of each individual circuit.  Then we have the LED lights corresponding with the correct colors of the stoplight.  These then connect to resistors which reduce the flow of electrical current.  The resistors are added so that the LEDs don’t receive too much current at once and short out.


![IMG_9C6E77CA6CEA-1](https://user-images.githubusercontent.com/59840208/190528723-4b9b0029-81e7-4cfe-8f9b-7a4887b25c0a.jpeg)
Figure 3

![IMG_7234117E4D1C-1](https://user-images.githubusercontent.com/59840208/190528744-e8445f7e-f765-480c-9247-17b623574c22.jpeg)
Figure 4

For this lab, Flask and python were used to connect between the physical components and the webpage and control the functionality.  Flask was installed on the raspberry pi and the file structure was as follows:

Webapp (folder)
* App.py (python file)
** This file contains all of the python script that allows the GPIO pins to be configured
* Static (folder)
** Style.css (css file)
*** This file contains the majority of css styles for the web page.  It created a nice usable interface for the user to work with
* Templates (folder)
** Main.html (html file)
*** This file contains the HTML needed to provide content to the page.  Some lines within this allow the app.py file to understand what functionality needs to be provided at any point in the program.

The python file is were we control the GPIO pin output and inputs.  The program begins by importing needed libraries (such as RPi.GPIO). It then sets the mode to BCM (Broadcom soc channel).  This allows us to refer to the pin by the GPIO numbers (changes depending on what version of raspberry pi is used) rather than the pin number (which would be BROAD instead of BCM).  See the appendix for a schematic of the pins for the raspberry pi used in this lab.  The program then uses GPIO.setup(pin, OUT)command to set up each pin used which prepares the pins to be given input.  For this lab, the pins are also initialized to LOW since the boards initial state is off.  

From here, the html file calls different methods depending on what button is pushed on the webpage.  This connects to our python file passing in the pressed pin number and the state of the pin (on or off).  Depending on the state, the program will cycle through the pins and set the pins HIGH or LOW depending on the passed state (LOW by default).  

If the off parameter is passed, all variables controlling threads will be set accordingly to “stop the thread”. 

 If the cycle parameter is passed, a second thread will start which will allow the loop controlling the cycling of the LEDs.  This is done in a separate thread so that the cycling can eventually stop.  If we did this in the main function, we would never be able to break the loop but we can stop the thread in main through boolean functions if it runs separately from the main thread.

## Thought Questions
* What language did you use for implementing this lab?  Why?
** I used python because it works very nicely with Flask and allows me to import useful libraries.  It is also very friendly to work with.
* What is the purpose of the resistor in this lab?
** The resistor reduced the flow of the current to the LED.  Without it, the LED would short circuit.
* What are practical applications of this project and what modifications would you make?
** This wouldn’t work super great for an actual stoplight as security concerns are involved but it is useful for any remote control device.  It would be useful for any other uses of lights that need to be controlled remotely such as lights within a large building or something used for a game such as red light green light.
* Time spent
** I spent 8-10 hours on this lab

## References

Setting up a web server with Flask:  https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/0

Learning how to control the GPIO pins with Flask:  https://randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/

Seeing examples of this project:  https://projects.raspberrypi.org/en/projects/physical-computing

Help with understanding threads: Steve Palica, IT&C undergraduate student

Help with debugging my code: Berin Hamilton (Ellsworth), IT&C undergraduate student

GPIO Pin layout for RaspberryPi 3: https://learn.sparkfun.com/tutorials/raspberry-gpio/gpio-pinout



