from utils import get_type_of_movement, connectSerial, Angles
import serial, time
from asgard import SerialThreadClass
import sys

s0 = serial.Serial()
ang_obj = Angles()
SerialThreadClass = SerialThreadClass()
# SerialThreadClass.serialSignal.connect()

# typeOfMovement, feedRate = get_type_of_movement()
baudrate = '115200'

s0 = connectSerial(s0)
i = 0
if s0.isOpen():
    while True:
        if "-ik" in sys.argv:
            angles = ang_obj.ask_ik()
            print(angles)
            break
        elif "-demo" in sys.argv:
            angles = ang_obj.give_position(i)
            i += 1
            print("Please press ENTER when ready...")
            input()
        else:
            angles = ang_obj.ask_angles()
        message = "G1 " + "A" + str(angles[0]) + " B" + str(angles[1]) + " C" + str(angles[1]) + \
            " D" + str(angles[2]) + " X" + str(angles[3]) + " Y" + str((angles[4] + angles[5])) + \
            " Z" + str(round(-angles[4] + angles[5], 2)) + " F150.0"
        messageToSend = message + "\n"
        time.sleep(0.5)
        s0.write(messageToSend.encode('UTF-8'))
        print("Send message:" + messageToSend)
else:
    print("No serial Connection")

s0.close()
