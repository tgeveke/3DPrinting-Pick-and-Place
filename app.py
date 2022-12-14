class app():
    def __init__(self, robot=True, camera=True, gcode=True, gcodeFileName='TestData/GCode/bency-gcode.gcode', bbox=True,
                 ml=True, printer=True):
        import sys
        if robot:
            from RobotClass import Robot
            self.Robot = Robot()
        if camera:
            from CameraClass import Camera
            self.Camera = Camera(save=True, stream=False, delay=10)
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

    def moveToLocation(self, x, y, z):
        self.Robot.move2target(x, y, z)

    def grab2droppoff(self, width, angle):
        self.Robot.grab(endPos=width, angle=angle)
        self.Robot.dropOff()

    def printer2robot(self, pos, imgsize):
        cam_x, cam_y, cam_z = pos

        scale = 0.4
        imglength = imgsize[0]
        imgheight = imgsize[1]

        relx = -295 + (scale * (cam_y - (imgheight / 2)))
        rely = 410 + (scale * (cam_x - (imglength / 2)))
        zoffset = 110

        return [relx, rely, cam_z + zoffset]

    def getMLoutput(self, imgName='TestData\Images\sample_6b26ca74_1_color.jpg'):
        output = self.model.predict(imgName, confidence=40, overlap=30).json()['predictions']  # [0]
        if len(output) > 0:
            # Get values from model
            x = output[0]['x']
            y = output[0]['y']
            return [x, y]
        else:
            print('No prediction made')
            return


if __name__ == '__main__':
    print('Running App')
    obj = app(robot=True, camera=True, gcode=True, bbox=True, ml=True, printer=False)
    obj.Robot.view_topPrinter()

    imgs = obj.captureImage(save=True)
    colorImg = imgs[0]
    imgname = imgs[2]
    print('Saved image at:', imgname)

    imgwidth = len(colorImg[0])
    imglength = len(colorImg)
    print('Image Size =', imgwidth, imglength)

    GCode_avgXYZ = obj.avgGCode()
    # print(GCode_avgXYZ)
    GCodex = GCode_avgXYZ[0]
    GCodey = GCode_avgXYZ[1]
    GCodez = GCode_avgXYZ[2]

    MLoutput = obj.getMLoutput(imgName=imgname)
    while MLoutput is None:
        print('ML error')
        imgs = obj.captureImage(save=True)
        colorImg = imgs[0]
        imgname = imgs[2]
        print('Saved image at:', imgname)
        MLoutput = obj.getMLoutput(imgName=imgname)

    print('Machine Learning Output (x, y):', MLoutput)
    mlx = MLoutput[0]
    mly = MLoutput[1]

    bbox = obj.getBoundingBoxes(colorImg, plot=True)
    while len(bbox) == 0:
        bbox = obj.getBoundingBoxes(colorImg, plot=True)

    thresh = 15
    for rectangle in bbox:
        xy = rectangle[0]
        print(xy)
        x = xy[0]
        y = xy[1]
        if int(x) in range(int(mlx) - thresh, int(mlx) + thresh) and int(y) in range(int(mly) - thresh, int(mly) + thresh):
            print('Found matching point')
            angle = round(rectangle[2], 2)
            print('Angle =', angle)

            scale = 4
            widths = rectangle[1]
            if scale * min(widths) > 800:
                print('Part too large')
            else:
                width = scale * min(widths)
                print('Width =', width)

            [x, y, z] = obj.printer2robot(pos=[mlx, mly, 10], imgsize=[imgwidth, imglength])
            print(x, y, z)
            if int(x) in range(-350, -150) and int(y) in range(350, 500):
                obj.moveToLocation(x=x, y=y, z=z)
                obj.grab2droppoff(width=width, angle=90 + angle)
            obj.Robot.home()
            exit()
