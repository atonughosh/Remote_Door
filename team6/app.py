#code to operate door lock through UI in a browser. This uses the index.html in /templates directory to generate the UI.

import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
pins = {
   5 : {'name' : 'Pin 5', 'state' : GPIO.LOW}   #Pin 5 in BCM numbering is confured to operate the actuator
   }

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
   return render_template('index.html', **templateData)

#code to turn pin 5 On and Off
@app.route("/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   deviceName = pins[changePin]['name']
   if action == "on":
      GPIO.output(changePin, GPIO.HIGH)
      message = "Turned " + deviceName + " on."       #Turn pin 5 On
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."      #Turn pin 5 Off
   if action == "toggle":
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."

   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   templateData = {
      'message' : message,
      'pins' : pins
   }

   return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)

