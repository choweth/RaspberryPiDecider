# Accelerometer class creation

class Accelerometer:

    def __init__(self, xAccl=0, yAccl=0, zAccl=0):
        self.xAccl=xAccl
        self.yAccl=yAccl
        self.zAccl=zAccl

    def printData(self):
        print("Acceleration in x is " + str(self.xAccl))
        print("Acceleration in y is " + str(self.yAccl))
        print("Acceleration in z is " + str(self.zAccl))

    def printCoord(self):
        print("(" + str(self.xAccl) + " ," + str(self.yAccl) + " ," + str(self.zAccl) + ")")

    def change(self):
        if self.zAccl > 200:
            return False
        else:
            return True
