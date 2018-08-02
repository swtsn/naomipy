# NaomiPy
Yet another take on using a Raspberry Pi & the Adafruit LCD board to control a Naomi hardware system.

I decided to reinvent the wheel for fun. Currently functional with its only feature being the ability to load to the game to the destination device.

TODO
----
* Currently the game uploads fine, but the display gives no output
* There is a bug where on the "Game Select" screen, if you click SELECT, it takes you to "Choose target device"
* Refactor the quick display functions
* Implement socket test
* States probably don't need to have the lcd as a member
* Awkward creation of Uploader, try to refactor (new_menu is messy)
* Fix & improve logging
* Turn off LCD on exit
* Configuration solution
* UI enhancements
* Status propagation for writing game to DIMM
* Fix game list
* Figure out when an Atomiswave game won't let us load another game
* Proper packaging and distribution
* Generalize lcd to 'display' so that testing interfaces can be more easily written
