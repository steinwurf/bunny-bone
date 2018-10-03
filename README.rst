Bunny Bone
==========
.. image:: ./icon.png

This project contains the Arduino (Simblee) code for a data collector which uses
Bluetooth Low Energy (BLE) to communicate readings from a sensor.
Using the python library `gatt <https://github.com/getsenic/gatt-python>`_ the
readings are received and written to a file.

The project is very specialized but may be a good example for working with BLE.

Setup bunny bone python application
-----------------------------------

Disclaimer: The bunny bone python application will only run on Linux, and has
only been run on Ubuntu 18.04.

1. Install the dependencies::

    sudo apt-get update
    sudo apt-get install virtualenv python3-pip libdbus-1-dev libglib2.0-dev libgirepository1.0-dev libcairo2-dev git

2. Clone the project::

    git clone https://github.com/steinwurf/bunny-bone


3. Setup the virtual environment::

    cd bunny-bone
    virtualenv -p python3 bluetooth
    source bluetooth/bin/activate
    pip3 install -r requirements.txt

Install the bunny bone desktop launcher
---------------------------------------

Run the following command to install the desktop shortcut and result directory::

    ./install.sh

Now click the new bunny bone icon on the desktop and allow it to execute.

A terminal should show and the results will appear in the
`~/Desktop/bunny-bone-results` folder.

Configuration File
------------------

If you need to configure the python application, you can do so by changing the
`conf.cfg` file.

The configuration file consists of various sections.

DEFAULT section
...............
The DEFAULT section specifies the adapter name to use. This is the adapter name
of the bluetooth device you want to use. You can use this command to get the
name::

    hcitool dev

Example output::

    Devices:
        hci0	00:1C:DE:07:4D:30

Here the name is hci0.

Sensor Sections
...............
Following the DEFAULT section is a set of one or more sensor sections.
The name of each section is the name of the device which we want to read from.
Each sensor section contains an attribute called OutputFile which is the file
which will used to store the results for that sensor.

Please restart the application for the applied changes to take effect.

Simblee
-------
The Arduino code is made for the Simblee board.

Library requirements:

1. CircularBuffer library from Library Manager.
2. HX711 library from github: https://github.com/bogde/HX711

Description of data
-------------------
The readings received by the python console application are stored in the
specified output file.
The readings stored as a comma separated file (csv). Such files are supported
by many spreadsheet applications such as Microsoft Excel or Google Sheets.

The Simblees notion of time is based of when it was powered on.
This means that it's not possible for the Simblee to know the absolute time of a
reading. Instead it transmit the time it took the reading and the time it send
it to the python script. Using this information and the computer's clock it's
possible to convert the Simblee's timestamp to an absolute time.

The following information is stored for each reading:

* `Read Time` the Simblee timestamp for when the reading was performed in ms.
* `Send Time` the Simblee timestamp for when the reading was sent in ms.
* `Current Time` the computer's timestamp in ms since Jan 01 1970.
* `Time` an absolute timestamp of when the reading calculated using the previous
  3 values. The resolution of this timestamp is in seconds. If more precision
  is needed use the previous 3 values.
* `Reading` the value read by the Simblee in grams or degrees depending on mode.
  Note: this value can occasionally "spike" where the readings are
  incorrectly either very large or small. During a 16 hour measurement
  with ~4000 readings 5 spikes occurred.
* `Sequence Number` a value incrementing with each reading. Can be useful for
  determining if a reading was somehow lost.
  Note: this value will reset when the power to the arduino is cut.

So all in all if you only need to work with absolute timestamps and the readings
you can just use the `Time` and `Reading` values.
