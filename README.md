# PyAmsSerial
Python library for controlling VU-AMS (5FS) via IR to USB cable (serial infrared spacelabs cable) for use with Windows.

## What is it?
A way to start and stop recordings on-, and to send markers with a custom message to the 5FS AMS device. 

## Version and Dependencies
PyAmsSerial is test to work with python 3.6 up to 3.11.1. Since it has few dependencies it is likely to function properly for at least some future versions of python. If you run in to any errors, please let me know! (q.s.r.madari@vu.nl)

The code is dependent on pyserial, subprocess, json and zlib. Of these only pyserial is not included by default. 
When installing pyserial be sure to use `pip install pyserial` and not `pip install serial`, as this is a package with a conflicting import name.

## Usage
Place the PyAmsSerial.py file in your python project folder. Implement it into your code as desired using
`import PyAmsSerial`
And follow the instructions in it's `main` function:

### Open a connection to AMS device using
    `connection = AmsSignal()`
Please be sure only one AMS IR-cable is connected to the PC.
An attempt will be made to find the connected COM port automatically.
If multiple devices with the name 'USB Serial Port' are connected to the PC, the first device matching this name will be used as AMS device.

### Forcing a COM port
The COM port can be found in the windows Device Manager (Right click on the Windows Start menu, select Device Manager)
- Be sure the IR-cable is connected
- Locate 'Ports (COM & LPT)' and look up a name matching 'USB Serial Port COM3', where COM3 could be COM7 or any other.
With this number you can force the AMS connection to use this port.

    `com = 'COM3' # Or any other number you found`
    `connection = AmsSignal(port=com)`

### After connecting, start the AMS Recording with
    `connection.start()`

### Send a marker containing your custom message using
    `connection.messageMarker(message = "your message")`

### Stop the recording using
    `connection.stop()`

### And finish by closing the connection
    `connection.close()`
> This port can't be re-opened as long as it isn't closed or the AMS IR-cable is physically disconnected.

