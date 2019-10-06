import numpy as np

PI = 3.141592654
Rad = PI / 180
Grad = 180. / PI

#Size of parts
AlturaH = 202
LongBrazo = 160
LongAntBr = 195 + 67.15
LongMunec = 100

def inverseK(Xreal, Yreal, Zreal, alfa1, beta1, gamma1):
    # gamma1 = 180

    # orientation matrix parameters
    cosalfa1 = np.cos(alfa1 * Rad)
    senalfa1 = np.sin(alfa1 * Rad)
    cosbeta1 = np.cos(beta1 * Rad)
    senbeta1 = np.sin(beta1 * Rad)
    cosgamma1 = np.cos(gamma1 * Rad)
    sengamma1 = np.sin(gamma1 * Rad)

    # X-Y-Z SET ANGLES
    # X'
    r11 = (cosalfa1 * cosbeta1)
    r21 = (senalfa1 * cosbeta1)
    r31 = -senbeta1
    # Y'
    r12 = (cosalfa1 * senbeta1 * sengamma1) - (senalfa1 * cosgamma1)
    r22 = (senalfa1 * senbeta1 * sengamma1) + (cosalfa1 * cosgamma1)
    r32 = (cosbeta1 * sengamma1)
    # Z'
    r13 = (cosalfa1 * senbeta1 * cosgamma1) + (senalfa1 * sengamma1)
    r23 = (senalfa1 * senbeta1 * cosgamma1) - (cosalfa1 * sengamma1)
    r33 = (cosbeta1 * cosgamma1)

    a2 = LongBrazo
    d4 = LongAntBr + LongMunec / 2
    d6 = LongMunec / 2 # + LongTool / 2

    #  d4 = LongAntBr
    #  d6 = LongMunec + LongTool
    a22 = a2 * a2
    d42 = d4 * d4
    # int d = 0

    xc = Xreal - d6 * r13
    yc = Yreal - d6 * r23
    zc = (Zreal - AlturaH) - d6 * r33

    x2 = xc * xc
    y2 = yc * yc
    z2 = zc * zc
    # d22 = d * d

    # Calculate theta1
    theta1 = (np.arctan2(yc, xc)) * Grad

    # Calculate theta3
    K = (x2 + y2 + z2 - a22 - d42) / (2 * a2)
    Raiz3 = np.sqrt(np.abs(np.abs(d42) - (K * K)))

    #  Raiz3 = np.sqrt(Mathf.Abs(d42) - (K * K))
    theta3 = -(np.arctan2(K, Raiz3)) * Grad

    costheta1 = np.cos(theta1 * Rad)
    sentheta1 = np.sin(theta1 * Rad)
    costheta3 = np.cos(theta3 * Rad)
    sentheta3 = np.sin(theta3 * Rad)

    Y = (-a2 * costheta3) * zc - (costheta1 * xc + sentheta1 * yc) * (d4 - a2 * sentheta3)
    X = ((a2 * sentheta3 - d4) * zc + (a2 * costheta3) * (costheta1 * xc + sentheta1 * yc))

    # Calculate theta2
    theta23 = (np.arctan2(Y, X)) * Grad
    theta2 = theta23 - theta3
    costheta2 = np.cos(theta2 * Rad)
    sentheta2 = np.sin(theta2 * Rad)

    costheta23 = (costheta2 * costheta3) - (sentheta2 * sentheta3)
    sentheta23 = (sentheta2 * costheta3) + (costheta2 * sentheta3)

    # Calculate theta4
    Y = ((costheta1 * r23) - (sentheta1 * r13))
    X = (-(costheta1 * costheta23 * r13) - (sentheta1 * costheta23 * r23) + (sentheta23 * r33))

    theta4 = (np.arctan2(Y, X)) * Grad
    costheta4 = np.cos(theta4 * Rad)
    sentheta4 = np.sin(theta4 * Rad)

    # Calculate theta5
    Y = (-r13 * ((costheta1 * costheta23 * costheta4) + (sentheta1 * sentheta4)) - r23 * ((sentheta1 * costheta23 * costheta4) - (costheta1 * sentheta4)) + r33 * (sentheta23 * costheta4))
    X = (-r13 * (costheta1 * sentheta23) - r23 * (sentheta1 * sentheta23) - r33 * (costheta23))

    theta5 = (np.arctan2(Y, X)) * Grad
    costheta5 = np.cos(theta5 * Rad)
    sentheta5 = np.sin(theta5 * Rad)

    # Calculate theta6
    Y2 = (-r11 * ((costheta1 * costheta23 * sentheta4) - (sentheta1 * costheta4)) - r21 * ((sentheta1 * costheta23 * sentheta4) + (costheta1 * costheta4)) + r31 * (sentheta23 * sentheta4))
    X61 = (costheta1 * costheta23 * costheta4 + sentheta1 * sentheta4) * costheta5 - (costheta1 * sentheta23 * sentheta5)
    X62 = (sentheta1 * costheta23 * costheta4 - costheta1 * sentheta4) * costheta5 - (sentheta1 * sentheta23 * sentheta5)
    X63 = sentheta23 * costheta4 * costheta5 + costheta23 * sentheta5
    X2 = r11 * X61 + r21 * X62 - r31 * X63

    theta6 = (np.arctan2(Y2, X2)) * Grad
    costheta6 = np.cos(theta6 * Rad)
    sentheta6 = np.sin(theta6 * Rad)

    #  return all calculated angles
    return [theta1, theta2, theta3, theta4, theta5, theta6]


def main():
    print(inverseK(10., 0., 0., 0., 0., 0.))

if __name__ == '__main__':
    main()
