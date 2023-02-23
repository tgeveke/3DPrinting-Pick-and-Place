# G Code Parser
# Tom Geveke
# CAIS Lab, Penn State 2022

class GCodeParser:
    import numpy as np
    import matplotlib.pyplot as plt

    def __init__(self, fileName: str, 
                       allPoints: bool = False, 
                       maxRuns: int = 100000, 
                       plot: bool = False,
                        save: bool = False):
        print('GCodeParser class __init__()')
        
        if allPoints: 
            self.maxRuns = self.numLines
        else: 
            self.maxRuns = maxRuns
        self.plot = plot
        self.save = save

        try:
            with open(fileName, 'r') as gcodeFile:
                print(f'File: {fileName} opened successfully')
                self.lines = gcodeFile.readlines()
        except FileNotFoundError:
            print(f'{fileName} not found in GCodeParser, exiting')
            exit()
        self.fileName = fileName
        self.numLines = len(self.lines)
        print('Number of lines =', self.numLines)
        self.parse()

    def parse(self):
        print('Parsing file for entries =', self.maxRuns)
        self.points = []
        index = 0
        z = 0

        for i in range(self.maxRuns):
            line = self.lines[i]
            words = line.split(' ')
            if words[0] == 'G1':
                if index < self.maxRuns:
                    index += 1
                    for word in words[1:]:
                        firstLetter = word[0]
                        if firstLetter == 'X':
                            try:
                                x = float(word[1:])
                            except:
                                continue
                        elif firstLetter == 'Y':
                            y = float(word[1:])
                        elif firstLetter == 'Z':
                            z = float(word[1:])
                            lastZ = z
                if 'z' not in locals():
                    z = lastZ
                if 'x' in locals() and 'y' in locals():
                    self.points.append([x, y, z])

    def averageXYZ(self, precision = 3):
        if self.points is not None:
            print('Getting average (x, y, z)')

            allX = [point[0] for point in self.points]
            allY = [point[1] for point in self.points]
            allZ = [point[2] for point in self.points]

            avgX = round(sum(allX) / len(allX), precision)
            avgY = round(sum(allY) / len(allY), precision)
            avgZ = round(sum(allZ) / len(allZ), precision)
            return (avgX, avgY, avgZ)

    def graph3D(self):  
        from mpl_toolkits import mplot3d
                
        plot = self.plt.axes(projection='3d')
        
        xdata = [point[0] for point in self.points]
        ydata = [point[1] for point in self.points]
        zdata = [point[2] for point in self.points]
        
        plot.set_xlabel('X')
        plot.set_xlim(0, 250)
        plot.set_ylabel('Y')
        plot.set_ylim(0, 250)
        plot.set_zlabel('Z')
        plot.set_zlim(0, 250)
        
        plot.scatter3D(xdata, ydata, zdata, c=zdata, cmap='prism');
        self.plt.show()

    def plot2D(self):        
        xdata = [point[0] for point in self.points]
        ydata = [point[1] for point in self.points]
        
        fig = self.plt.figure()
        self.plt.xlabel ='X'
        self.plt.xlim = (0, 250)
        self.plt.ylabel = 'Y'
        self.plt.ylim = (0, 250)
        
        # Plot
        self.plt.plot(xdata, ydata)
        self.plt.title('2D Overhead Graph')
        
        # Check if you want to show
        if self.plot:
            self.plt.show() 

        # Check if you want to save
        if self.save:
            # Save image
            from os import path
            save_name = path.splitext(self.fileName)[0] + '_overhead2D.png'
            fig.savefig(save_name) 
            print(f'Saved image at file: {save_name}') 
            return save_name    

    def cluster2D(self, numPoints = 12000, thresh = 25):
        import scipy.cluster.hierarchy as hcluster

        xdata = [point[0] for point in self.points][:-(len(self.points) - numPoints)]
        ydata = [point[1] for point in self.points][:-(len(self.points) - numPoints)]
        data = self.np.column_stack((xdata, ydata))
        
        # Clustering
        clusters = hcluster.fclusterdata(data, thresh, criterion="distance")

        # Plotting
        if self.plot:
            self.plt.scatter(*self.np.transpose(data), c=clusters)
            title = f'Clustering: Threshold: {round(thresh, 3)}, Number of clusters: {len(set(clusters))}'
            self.plt.title(title)
            self.plt.show()     
        if self.save:
            # Save image
            from os import path
            self.plt.gcf()
            self.plt.savefig(path.splitext(self.fileName)[0] + '_2Dcluster.png')
        return clusters
   
if __name__ == "__main__":
    # ----- TESTING ----- #
    import time
    start_time = time.time()

    gcode_file_name = r'TestData\GCode\bency-gcode.gcode'

    obj = GCodeParser(fileName=gcode_file_name, allPoints=False, maxRuns=100000, plot=True, save=True)
   
    total_time = round(time.time() - start_time, 3)
    print(f'Runtime = {total_time} seconds')

    # --- Check Class Methods --- #
    # obj.graph3D()
    obj.cluster2D()
    obj.plot2D()
