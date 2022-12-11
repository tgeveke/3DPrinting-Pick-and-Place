class app():
    def __init__(self, robot=True, camera=True, gcode=True, gcodeFileName = 'TestData/GCode/bency-gcode.gcode', bbox=True, ml=True, printer=True):
        import sys
        if robot:
            from RobotClass import Robot
            self.Robot = Robot()
        if camera:
            from CameraClass import Camera
            self.Camera = Camera(save=True, stream=False)
        if gcode:
            from GCodeParserClass import GCodeParser
            self.GCodeParser = GCodeParser(fileName=gcodeFileName)
        if bbox:
            from BoundingBoxClass import BoundingBox
            self.BoundingBox = BoundingBox()
        if ml:
            from roboflow import Roboflow
            rf = Roboflow(api_key="HNYW73nuLKdWCzXEO2EC")
            project = rf.workspace("cias-lab").project("data-set-r52g6")
            self.model = project.version(1).model
        if printer:
            from PrinterClass import Printer
            self.Printer = Printer()

    def captureImage(self, save):
        return self.Camera.capture(save=save)  # rgb_array, depth_array

    def clusterGCode(self):
        clusters = self.GCodeParser.cluster2D()
        print(clusters[1])
    
    def avgGCode(self):
        avgs = self.GCodeParser.averageXYZ()
        return avgs
    
    def getBoundingBoxes(self, img, plot=True):
        return self.BoundingBox.findBBoxes(img=img, plot=plot)
    
    def moveToLocation(self, x, y, z, angle):
        self.Robot.move2target(x, y, z, angle)

    def printer2robot(self, pos):
        rob_x, rob_y, rob_z = pos
        xoffset = -630
        yoffset = 150
        zoffset = 100
        return [rob_x+xoffset, rob_y+yoffset, rob_z+zoffset]


    def getMLoutput(self, imgName='TestData\Images\sample_6b26ca74_1_color.jpg'):
        output = self.model.predict(imgName, confidence=40, overlap=30).json()['predictions'] #[0]
        if len(output) > 0:
            # Get values from model
            x = output[0]['x']
            y = output[0]['y']

            return [x, y]
        else:
            print('No prediction made')
            return

    def readInstructions(self, filename = 'instructions.txt'):
        options = {
            'wait': wait,
            'reset': reset,
            'go home': home,
            'view front printer': view_frontPrinter,
            'view top printer': view_topPrinter,
            'capture image': captureImage,
            'move to target position': move2target,
            'grab': grab,
            'view object top': viewObjectTop,
            'get front distance': getFrontDistance
        }

        args = self.sys.argv()
        print(args)
        if len(args) > 1:
            fileName = args[1]
            try:
                file = open(filename)
            except:
                print('Error opening file:', fileName)
        for instruction in file.readlines():
            if '#' not in instruction:  # Skips 'commented out' lines of instruction
                print(instruction)
                options[instruction.strip()]()

if __name__ == '__main__':
    print('Running App')
    obj = app(robot=True, camera=True, gcode=True, bbox=True, ml=True, printer=False)

    imgs = obj.captureImage(save=True)
    colorImg = imgs[0]
    imgname = imgs[2]

    # imgname = 'TestData/Images/sample_6b26ca74_1_color.jpg'
    MLoutput = obj.getMLoutput(imgName=imgname)
    print(MLoutput)
    mlx = MLoutput[0]
    mly = MLoutput[1]

    GCode_avgXYZ = obj.avgGCode()
    # print(GCode_avgXYZ)
    GCodex = GCode_avgXYZ[0]
    GCodey = GCode_avgXYZ[1]
    GCodez = GCode_avgXYZ[2]

    avgx = (mlx + GCodex) / 2
    avgy = (mly + GCodey) / 2
    thresh = 5

    colorImg = obj.BoundingBox.openImg(imgname)
    bbox = obj.getBoundingBoxes(colorImg, plot=True)
    for rectangle in bbox:
        xy = rectangle[0]
        x = xy[0]
        y = xy[1]
        if int(x) in range(int(mlx) - thresh, int(mlx) + thresh) and int(y) in range(int(mly) - thresh, int(mly) + thresh):
            print('Found')
            print(xy)
            angle = round(rectangle[2], 2)
            print(angle)

            scale = 6.15
            widths = rectangle[1]
            if scale*min(widths) > 800:
                print('Part too large')
            else:
                width = scale * min(widths)
                print(width)
            [x, y, z] = obj.printer2robot(pos=[mlx, mly, GCodez])
            print(x, y, z)
            obj.moveToLocation(x=x, y=y, z=z, angle=-angle)
            obj.Robot.grab(endPos=width)
            obj.Robot.home(speed=50)

