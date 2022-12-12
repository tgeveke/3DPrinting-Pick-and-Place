class BoundingBox():
    import cv2
    import numpy as np

    def __init__(self):
        print('Bounding Box class __init__()')

    def openImg(self, fileName):
        try:
            img = self.cv2.imread(fileName)
            return img
        except:
            print('Error opening file:', fileName)
            return

    def cropImage(self, img):
        croppedImg = img[0:480, 0:640]  # Crop region of interest
        return croppedImg

    def blurImg(self, img):
        blurredImg = self.cv2.GaussianBlur(img, (5, 5), 0)
        return blurredImg

    def findEdges(self, img):
        img_edges = self.cv2.Canny(img, 60, 80)
        return img_edges

    def findBBoxes(self, img, plot, areaThresh=3000):
        img_edges = self.findEdges(self.blurImg(img))  # Use self.blurImg(img)) to slightly blur the image
        self.cv2.imshow('Edges', img_edges)
        contours, _ = self.cv2.findContours(img_edges, self.cv2.RETR_EXTERNAL, self.cv2.CHAIN_APPROX_SIMPLE)
        rectangles = []

        # Approximate contours to polygons + get bounding rects and circles
        for contour in contours:
            rectangle = self.cv2.minAreaRect(contour)
            area = rectangle[1][0] * rectangle[1][1]  # Length x width
            if 100000 > area > areaThresh:
                rectangles.append(rectangle)  # For returning values
                angle = self.np.int0(rectangle[2])
                box = self.np.int0(self.cv2.boxPoints(rectangle))
                if plot:
                    self.cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
                    self.cv2.putText(img, 'Angle = ' + str(angle), (box[0][0], box[0][1]),
                                     self.cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        if plot:
            self.cv2.imshow('Bounding Boxes', img)
            self.cv2.waitKey(0)

        self.rectangles = rectangles
        return rectangles

    def getAngles(self):
        angles = []
        for rectangle in self.rectangles:
            angles.append(rectangle[2])
        return angles


if __name__ == '__main__':
    obj = BoundingBox()
    img_fileName = 'sample_f065f939/sample_f065f939_1_color.jpg'  # 'TestData/GCode/other-test-gcode.png' # 'TestData/Images/sample_6b26ca74_1_color.jpg'
    img = obj.openImg(img_fileName)
    boundingBoxes = obj.findBBoxes(img, plot=True)
