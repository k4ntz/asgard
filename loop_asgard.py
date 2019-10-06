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
    print("")
    while True:
        # First position     ##### FOR THE GREY ONE, DO NOT USE 4th one !
        angles = [20, 0, 0, 0, 0, 0]
        angles = [round(angles[0] / 6, 2), angles[1], angles[2], angles[3],
                round(angles[4] / 13, 2), round(angles[5] / 3.33, 2)]
        message = "G0 " + "A" + str(angles[0]) + " B" + str(angles[1]) + " C" + str(angles[1]) + \
            " D" + str(angles[2]) + " X" + str(angles[3]) + " Y" + str((angles[4] + angles[5])) + \
            " Z" + str(round(-angles[4] + angles[5], 2))
        messageToSend = message + "\n"
        s0.write(messageToSend.encode('UTF-8'))
        time.sleep(7)

        # Second position
        angles = [0, 30, -30, 0, 0, 0]
        angles = [round(angles[0] / 6, 2), angles[1], angles[2], angles[3],
                round(angles[4] / 13, 2), round(angles[5] / 3.33, 2)]
        message = "G0 " + "A" + str(angles[0]) + " B" + str(angles[1]) + " C" + str(angles[1]) + \
            " D" + str(angles[2]) + " X" + str(angles[3]) + " Y" + str((angles[4] + angles[5])) + \
            " Z" + str(round(-angles[4] + angles[5], 2))
        messageToSend = message + "\n"
        s0.write(messageToSend.encode('UTF-8'))
        time.sleep(7)

        # Third position change gripper
        closing_percentage = 60
        message = "M3 S" + str((255 / 20) * closing_percentage)
        messageToSend = message + "\n"
        s0.write(messageToSend.encode('UTF-8'))
        time.sleep(7)

        # Fourth position change gripper
        closing_percentage = 20
        message = "M3 S" + str((255 / 20) * closing_percentage)
        messageToSend = message + "\n"
        s0.write(messageToSend.encode('UTF-8'))
        time.sleep(7)
else:
    print("No serial Connection")

s0.close()
