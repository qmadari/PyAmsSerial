import serial # pip install pyserial
import subprocess 
import json
from zlib import crc32

class AmsConnection:
    def __init__(self,port = 'auto') -> None:
        self.baud = 38400 # 5FS uses 38400
        self.port = port # windows: COM number
        self.bytesize = serial.EIGHTBITS # fivebits sixbits sevenbits eightbits
        self.parity = serial.PARITY_NONE # serial.PARITY_NONE # none space odd names mark even
        self.stopbits = serial.STOPBITS_ONE # one one_point_five two
        self.timeout = 1

        if self.port == 'auto':
           foundport = self.findAMSDevice()
           if foundport:
                print(f'AMS device found on {foundport}.')
                self.port = foundport

        self.ser = serial.Serial(self.port, self.baud, self.bytesize, self.parity, self.stopbits)

    def __appendCRC__(self,intbytearr):
        """All AMS communication ends with a CRC checksum"""

        ## original bytearray
        bytearr = bytearray(intbytearr)

        ## calculate CRC from bytearray and add as crc32
        crc = hex(crc32(bytearr))
        crcspl2 = [crc[i:i+2] for i in range(0, len(crc), 2)]  #crc[0] == '0x'
        crc32int = [int(ele,16) for ele in crcspl2[1:]]  #int(hex,base16))
        crc32int.reverse()
        for c32 in crc32int:
            intbytearr.append(c32)
        return intbytearr

    def __trunc32str2asc__(self,mes):
        """ Truncate any message longer than 32 to 32 characters in bytes """
        if len(mes) > 19:
            ascarr = [ord(ele) for ele in mes[:32]] # asc val for first 20 characters in mes
        else:
            zeros = [0 for _ in range(0,32)]
            ascarr = [ord(ele) for ele in mes]
            zeros[0:len(ascarr)] = ascarr[:]
            ascarr = zeros
        return ascarr

    def __create__(self, message = ""):
        """ Used in messagemarker """
        # primarybytes =  bytearray(b'\x38\x00\x0e\x00\x03\x00\x30\x00\x11\x11\x11\x11\x01\x00\x00\x00\x04\x00\x00\x00')
        b = [0 for _ in range(0,52)] # len(b) = 52, 52 0's
        b[0] = 56   # Size packet 0x38 = 56
        b[2] = 14   # Tag 0x0e = 14
        b[4] = 3    # wTag (I)
        b[6] = 48   # wSize 0x30 = 48
        b[8] = 17   # Clock tick (4 0x11 is een clock tick?) 0x11 = 17
        b[9] = 17   #
        b[10] = 17  #
        b[11] = 17  #
        b[12] = 1   # lType
        b[16] = 4   # lCode
        if not message == "":
            print(f'message: {message[:32]}')
            b[20:] = self.__trunc32str2asc__(message)[:]
        
        bytearr = self.__appendCRC__(b)
        return bytearr
        
    def __write__(self,bytearray):
        """ Used to actually send the packet """
        self.ser.write(bytearray)

    def findAMSDevice():
        dev = None
        target = None
        out = subprocess.getoutput("PowerShell -Command \"& {Get-PnpDevice | Where-Object {$_.FriendlyName -Like '*(COM*'} | Where-Object {$_.Status -Like '*OK*'} | Where-Object {$_.FriendlyName -Like '*USB Serial Port*'}  | Select-Object Status,Class,FriendlyName,InstanceId | ConvertTo-Json}\"")
        if out == '':
            print(f"'WARN: USB Serial Port' not found in serial devices list, AMS not available.")
            return dev
        j = json.loads(out)
        if type(j) is list:
            print(f"INFO: Multiple matches to 'USB Serial Port' have been found in devices list.")
            print(f"INFO: Only the first matching device will be returned. Check the Windows Device manager")
            dev = j[0]
        else:
            dev = j
        if dev:
            com = dev['FriendlyName'].split('(')[-1].rstrip(')')
            print(f"{com}, {dev['Status']}")
            target = com
        return target

    def close(self):
        """ Close the COM port """
        self.ser.close()

    def messageMarker(self,message = "message"):
        """ Send the a marker with a message """
        self.__write__(bytearray=self.__create__(message=message))

    def start(self):
        """ Send the Start Recording command """
        b = [0x08,0x00,0x0b,0x05]
        bytearr = self.__appendCRC__(b)
        self.__write__(bytearray=bytearr)
        print('AMS start')

    def stop(self):
        """ Send the Stop Recording command """
        b = [0x08,0x00,0x0b,0x06]
        bytearr = self.__appendCRC__(b)
        self.__write__(bytearray=bytearr)
        print('AMS stop')

def main ():

    ## Open a connection to AMS device using
    connection = AmsConnection()

    ## Close it using
    connection.close() # This port can't be re-opened as long as it isn't closed or the AMS IR-cable is physically disconnected

    ## The COM port can be found in the windows Device Manager (Right click on the Windows Start menu, select Device Manager)
    ## - Be sure the IR-cable is connected
    ## - Locate 'Ports (COM & LPT)' and look up a name matching 'USB Serial Port COM3', where COM3 could be COM7 or any other.
    ## With this number you can force the AMS connection to use this port.

    com = 'COM3' # Or any other number you found
    connection = AmsConnection(port=com)

    ## After connecting, start the AMS Recording with
    connection.start()
    # time.sleep(3) # import time
    
    ## Send a marker containing your custom message using
    connection.messageMarker(message = "your message")
    # time.sleep(3) # import time

    ## Stop the recording using
    connection.stop()
    # time.sleep(3) # import time

    ## And finish by closing the connection
    connection.close()

if __name__ == "__main__":
    main()