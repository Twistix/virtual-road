# Virtual road
This project aims to create a graphical interface connected to a home trainer to display the performance of the cyclist, and to simulate a real track by indicating the resistance setting to apply to simulate the slope.


## Description 
The product his divided in two main parts :
* The "sensor" part constituded of an arduino and differents sensors (principally an hall effect sensor placed on the bike to count each turn of the wheel)
* The main program developped in Python and communicating with the Arduino by USB. His goal is to calculate differents things and to display a graphical interface for the cyclist

First, we use the an hall effect sensor to count each turn of the rear wheel of the bike on the home-trainer. The Arduino calculate the actual speed of the cyclist and send recurently by USB the speed and the number of wheel revolution.

Then, at the beginning we load a course on the Python program. In the data of the course we have the slope as a function of the distance. So, the Python program recieve the data from the Arduino, it compares the actual travelled distance with the distance for the slope, and determine what slope the cyclist should be in if it was doing the course for real.

Thus it can indicate on the interface a resistance setting to be applied by the cyclist to simulate this slope.

Different other features uses the same principle. We have a little map of the course with a red dot indicating the cyclist where he is on the course. We have also differents real picures from google map that are displayed depending on the distance travelled.

  
## Demo
Here you can see a little demo of the project :

![demo_parcours](https://raw.githubusercontent.com/Twistix/virtual-road/main/images/demo_parcours.gif)
