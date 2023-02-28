# PyAmsSerial
Python library for controlling [VU-AMS](https://vu-ams.nl/) (5fs device) via IR to USB cable (serial infrared spacelabs cable) for use with Windows.

## What is it?
A way to start and stop recordings on-, and to send markers with a custom message to the 5fs AMS device. 

## Version and Dependencies
PyAmsSerial is test to work with python 3.6 up to 3.11.1. Since it has few dependencies it is likely to function properly for at least some future versions of python. If you run in to any errors, please let me know! (q.s.r.madari@vu.nl)

The code is dependent on pyserial, subprocess, json and zlib. Of these only pyserial is not included by default. 
When installing pyserial be sure to use `pip install pyserial` and not `pip install serial`, as this is a package with a conflicting import name.

## VU-DAMS
This code is intended only to send start, stop and marker commands to the AMS device. Concerning the actual device settings, please make sure you use a computer running the [VU-DAMS](https://vu-ams.nl/downloads/) to configure it as desired. The settings will be retained on the device when disconnected from this computer.

## Usage
Copy the PyAmsSerial.py file into your python project folder, then implement it into your own code as described below.

```python
import PyAmsSerial
```
And follow the instructions in it's `main` function:

### Open a connection to AMS device using
```python
connection = AmsConnection()
```
Please be sure only one AMS IR-cable is connected to the PC.
An attempt will be made to find the connected COM port automatically.
If multiple devices with the name 'USB Serial Port' are connected to the PC, the first device matching this name will be used as AMS device.

### Forcing a COM port
The COM port can be found in the windows Device Manager (Right click on the Windows Start menu, select Device Manager)
- Be sure the IR-cable is connected
- Locate 'Ports (COM & LPT)' and look up a name matching 'USB Serial Port COM3', where COM3 could be COM7 or any other.
With this number you can force the AMS connection to use this port.

```python
com = 'COM3' # Or any other number you found
connection = AmsConnection(port=com)
```

### After connecting, start the AMS Recording with
```python
connection.start()
```

### Send a marker containing your custom message using
```python
connection.messageMarker(message = "your message")
```

### Stop the recording using
```python
connection.stop()
```

### And finish by closing the connection
```python
connection.close()
```
    
Note: The used port can't be re-opened as long as it isn't closed in this way. Either keep this connection open during the whole session, or close it and reconnect to the AMS by making a new `AmsConnection()`to the same port when a new (series of) markers have to be sent.

