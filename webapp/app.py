import RPi.GPIO as GPIO
import sys
from threading import Thread
from time import sleep
from flask import Flask, render_template, request
app = Flask(__name__)

global theLoop
theLoop = False

GPIO.setmode(GPIO.BCM)

# Store pins in directory
pins = {
    17 : {'name' : 'GPIO 17', 'state' : GPIO.LOW},
    27 : {'name' : 'GPIO 27', 'state' : GPIO.LOW},
    22 : {'name' : 'GPIO 22', 'state' : GPIO.LOW}
}

# Set pins to off:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():

    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    templateData = {
        'pins' : pins
    }

    return render_template('main.html', **templateData)
    

@app.route("/<changePin>/<action>")
def action(changePin, action):
    
    changePin = int(changePin)
    
    def cycle():
        while theLoop:
                GPIO.output(17, GPIO.HIGH)
                sleep(2)
                if(isNotCycling):
                    break
                GPIO.output(17, GPIO.LOW)
                
                GPIO.output(27, GPIO.HIGH)
                sleep(2)
                if(isNotCycling):
                    break
                GPIO.output(27, GPIO.LOW)
                
                GPIO.output(22, GPIO.HIGH)
                sleep(2)
                if(isNotCycling):
                    break
                GPIO.output(22, GPIO.LOW)
    
    global isNotCycling
    
    isNotCycling = False
    
    thread = Thread(target = cycle)
    
    if action == "allBtnsOff":
        isNotCycling = True
        theLoop = False
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)

    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
    if action == "on":
        GPIO.output(changePin, GPIO.HIGH)
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
    
    if action == "cycle":
        theLoop = True
        thread.start()
            
            
    templateData = {
        'pins' : pins
    }
    
    return render_template('main.html', **templateData)
                    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
