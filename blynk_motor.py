var unlockedState = 1000;
var lockedState = 2200;

var locked = true
var motorPin = 14;
var buttonPin = 4

var Blynk = require('blynk-library');
var blynk = new Blynk.Blynk('ebc955d1eabc40cea069956d4826b062');
var v0 = new blynk.VirtualPin(0);

var Gpio = require('pigpio').Gpio,
  motor = new Gpio(motorPin, {mode: Gpio.OUTPUT}),
  button = new Gpio(buttonPin, {
    mode: Gpio.INPUT,
    pullUpDown: Gpio.PUD_DOWN,
    edge: Gpio.FALLING_EDGE
  })

v0.on('write', function(param) {
	console.log('V0:', param);
  	if (param[0] === '0') { //unlocked
  		unlockDoor()
  	} else if (param[0] === '1') { //locked
  		lockDoor()
  	} else {
  	}
});

function lockDoor() {
	motor.servoWrite(lockedState);
	locked = true

	//notify
  	//blynk.notify("Door has been locked!");
  	
  	//After 1.5 seconds, the door lock servo turns off to avoid stall current
  	setTimeout(function(){motor.servoWrite(0)}, 1500)
}

function unlockDoor() {
	motor.servoWrite(unlockedState);
	locked = false

	//notify
  	//blynk.notify("Door has been unlocked!"); 

  	//After 1.5 seconds, the door lock servo turns off to avoid stall current
  	setTimeout(function(){motor.servoWrite(0)}, 1500)
}

