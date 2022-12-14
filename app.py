class app():
    def __init__(self, robot=True, camera=True, gcode=True, gcodeFileName='TestData/GCode/bency-gcode.gcode', bbox=True, ml=True, printer=True, stl=False):
        print('App class __init__()')

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
        if stl:
            from STLParserClass import STLParser
            self.stlParser = STLParser()

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

        scale = 0.4 # [mm/px], from ~250mm/640px or ~220mm/480px
        imgLength = imgsize[0]
        imgHeight = imgsize[1]

        relx = -295 + (scale * (cam_y - (imgHeight / 2)))
        rely = 410 + (scale * (cam_x - (imgLength / 2)))
        zoffset = 110

        return [relx, rely, cam_z + zoffset]

    def getMLoutput(self, imgName='TestData\Images\sample_6b26ca74_1_color.jpg'):
        output = self.model.predict(imgName, confidence=40, overlap=30).json()['predictions']
        if len(output) > 0:
            # Get values from model
            x = output[0]['x']
            y = output[0]['y']
            return [x, y]
        else:
            print('No prediction made')
            return

    def run(self):
        self.Robot.view_topPrinter()

        imgs = self.captureImage(save=True)
        colorImg = imgs[0]
        imgname = imgs[2]
        print('Saved image at:', imgname)

        imgwidth = len(colorImg[0])
        imglength = len(colorImg)
        print('Image Size =', imgwidth, imglength)

        GCode_avgXYZ = self.avgGCode()
        # print(GCode_avgXYZ)
        GCodex = GCode_avgXYZ[0]
        GCodey = GCode_avgXYZ[1]
        GCodez = GCode_avgXYZ[2]

        MLoutput = self.getMLoutput(imgName=imgname)
        while MLoutput is None:
            print('ML error')
            imgs = self.captureImage(save=True)
            colorImg = imgs[0]
            imgname = imgs[2]
            print('Saved image at:', imgname)
            MLoutput = self.getMLoutput(imgName=imgname)

        print('Machine Learning Output (x, y):', MLoutput)
        mlx = MLoutput[0]
        mly = MLoutput[1]

        bbox = self.getBoundingBoxes(colorImg, plot=False)
        while len(bbox) == 0:
            bbox = self.getBoundingBoxes(colorImg, plot=False)

        thresh = 15
        for rectangle in bbox:
            bbox_xy = rectangle[0]
            print('Bounding box output (x,y):', bbox_xy)
            bbox_x = bbox_xy[0]
            bbox_y = bbox_xy[1]
            if int(x) in range(int(mlx) - thresh, int(mlx) + thresh) and int(y) in range(int(mly) - thresh, int(mly) + thresh):
                print('Found matching point')
                bbox_angle = round(rectangle[2], 2)
                print('Angle =', bbox_angle)

                scale = 4
                widths = rectangle[1]
                if scale * min(widths) > 800:
                    print('Part too large')
                else:
                    width = scale * min(widths)
                    print('Width =', width)

                [x, y, z] = self.printer2robot(pos=[mlx, mly, 10], imgsize=[imgwidth, imglength])
                print(x, y, z)
                if int(x) in range(-350, -150) and int(y) in range(350, 500):
                    self.moveToLocation(x=x, y=y, z=z)
                    self.grab2droppoff(width=width, angle=(90 + bbox_angle))
                self.Robot.home()
                exit()

if __name__ == '__main__':
    print('Running App')
    obj = app(robot=True, camera=True, gcode=True, bbox=True, ml=True, printer=False, stl=False)
    obj.run()

