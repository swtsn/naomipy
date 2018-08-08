# NaomiPy
Yet another take on using a Raspberry Pi & the Adafruit LCD board to control a
NAOMI hardware system.

I decided to reinvent the wheel for fun. Currently functional with its only
feature being the ability to load to the game to the destination device. The
game list has full support for NAOMI and Atomiswave games, and partial support
for NAOMI 2 games. There is no support for Chihiro or Triforce currently.

TODO
----
* Known bug: Flow gets messed up if it can't ping the selected DIMM
* Known bug: On the "Game Select" screen, if you click SELECT, it
  takes you to "Choose target device"
* Some full names need to be fleshed out
* Configuration solution
* Implement socket test
* States probably don't need to have the lcd as a member
* Fix & improve logging
* Turn off LCD on exit
* UI enhancements
* Status propagation for writing game to DIMM
* Figure out when an Atomiswave game won't let us load another game
* Proper packaging and distribution
* Generalize lcd to 'display' so that testing interfaces can be more easily
  written
