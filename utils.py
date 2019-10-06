from ik import inverseK
import serial_port_finder as spf

def get_type_of_movement():
    tom = "None"
    while tom[:2] not in ["G0", "G1"]:
        print("Give type of movement (G0/G1):")
        tom = "G0"
        if tom[:2] == "G1":
            print("Okay for G1, what feedrate ?")
            fr = "500"
            try:
                fr = str(float(fr))
                return "G1 ", fr
            except ValueError:
                tom = "None"
        elif tom[:2] == "G0":
            print("Okay for G0")
            return "G0 ", ""
        else:
            tom = "None"


def connectSerial(s0):
    serialPort = spf.serial_ports()[0]
    # serialPort = None
    baudrate = 115200
    if serialPort != "":
        s0.port = serialPort
        s0.baudrate = baudrate
        s0.timeout = 1
        # try:
        s0.close()
        s0.open()
        # except Exception as e:
        #     print("error opening serial port: " + str(e))
    else:
        print("There is not Serial Port value indicated to establish the connection.\n\
              Please check it and try to connect again.")
    return s0

class Angles():
    def __init__(self):
        self.angles = [0., 0., 0., 0., 0., 0.]
        self.possibles = ["x", "y", "z", "ax", "ay", "az"]
        self.pose = [0., 0., 0., 0., 0., 0.]

    def ask_angles(self):
        angle_number = None
        while True:
            self.print_current_state("angles")
            try:
                angle_number = input()
                if angle_number == "":
                    return [round(self.angles[0] / 6, 2), self.angles[1], self.angles[2], self.angles[3],
                            round(self.angles[4] / 13, 2), round(self.angles[5] / 3.33, 2)]
                angle_number = int(angle_number)
                if angle_number != 0:
                    print("Give an angle :")
                    angle_deg = float(input())
            except ValueError:
                print("Please give a number")
                continue
            self.angles[angle_number - 1] = angle_deg

    def give_position(self, number):
        # if number == 3:
        #     return [0., 0., 0., 0., 0., 0.]
        if number == 0:
            return [round(-20. / 6, 2), 0., 0., 0., round(85. / 13, 2), round(30. / 3.33, 2)]
        elif number == 1:
                return [round(-20. / 6, 2), 25., 0., 0., round(85. / 13, 2), round(30. / 3.33, 2)]
        elif number == 2 or number == 4:
            return [round(-20. / 6, 2), 25., 60., 0., round(85. / 13, 2), round(30. / 3.33, 2)]
        elif number == 3:
            return [round(-20. / 6, 2), 25., 110., 0., round(55. / 13, 2), round(30. / 3.33, 2)]
        # elif number == 4:
        #     return [-round(-20. / 6, 2), 0., 0., 0., round(80. / 13, 2), -round(30. / 3.33, 2)]
        # elif number == 5:
        #     return [-round(-20. / 6, 2), 90., 10., 0., round(80. / 13, 2), -round(30. / 3.33, 2)]
        else:
            exit()

    def ask_ik(self):
        axis = None
        while True:
            self.print_current_state("ik")
            axis = input()
            if axis == "":
                return inverseK(*self.pose)
            if axis not in self.possibles:
                print("Please give an axis within :" + str(self.possibles))
                continue
            idx = self.possibles.index(axis)
            if idx < 3:
                print("How much shift do you want along " + axis + "? :", end="")
            else:
                print("How much shift do you want around " + axis[-1] + "? :", end="")
            shift = input()
            try:
                shift = float(shift)
            except ValueError:
                print("Please give a number \n")
                continue
            self.pose[idx] = shift


    def print_current_state(self, typ):
        if typ == "angles":
            print("Current state:")
            for i, ang in enumerate(self.angles[:-1]):
                print(str(i + 1) + ": " + str(ang) + "°,   ", end='')
            print(str(len(self.angles)) + ": " + str(self.angles[-1]))
            print("Give angle number (1 - 6), ENTER to return:")
        elif typ == "ik":
            passed = False
            print("[ik] Current state:")
            for ax, axis in zip(self.possibles[:-1], self.pose[:-1]):
                if ax == "ax":
                    print("")
                    passed = True
                if passed:
                    print(ax + ": " + str(axis) + ",  ", end='')
                else:
                    print(" " + ax + ": " + str(axis) + ",  ", end='')
            print(self.possibles[-1] + ": " + str(self.pose[-1]))
            print("Give an axis, ENTER to return:")
