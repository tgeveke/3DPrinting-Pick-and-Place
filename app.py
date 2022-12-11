class app():
    def __init__(self, robot=True, camera=True, gcode=True, gcodeFileName = r'TestData\GCode\bency-gcode.gcode', bbox=True, ml=True, printer=True):
        import sys
        if robot:
            from RobotClass import Robot
            self.Robot = Robot()
        if camera:
            from CameraClass import Camera
            self.Camera = Camera(save=False)
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

    def captureImage(self):
        return self.Camera.capture()  # rgb_array, depth_array

    def clusterGCode(self):
        clusters = self.GCodeParser.cluster2D()
        print(clusters[1])
    
    def avgGCode(self):
        avgs = self.GCodeParser.averageXYZ()
        return avgs
    
    def getBoundingBoxes(self, img, plot=True):
        return self.BoundingBox.findBBoxes(img, plot)
    
    def xyangle_fromBBox(self, rectangle):
        return rectangle[0]
    
    def moveToLocation(self, x, y, z, angle):
        self.Robot.move2target(x, y, z, angle)

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
    obj = app(robot=True, camera=False, gcode=False, bbox=False, ml=False, printer=False)

    # imgs = obj.captureImage()
    # colorImg = imgs[0]
    # imgname = imgs[2]

    imgname = 'sample_a3d90371\sample_a3d90371_0_color.jpg'

    # MLoutput = obj.getMLoutput(imgName=imgname)
    # print(MLoutput)

    #colorImg = obj.BoundingBox.openImg(imgname)
    #bbox = obj.getBoundingBoxes(colorImg, plot=True)
    #for rectangle in bbox:
        # xyang_fromBBox = obj.xyangle_fromBBox(rectangle)
        # print(rectangle)
    
    # GCode_avgXYZ = obj.avgGCode()
    # print(GCode_avgXYZ)

