# Camera Class
# Tom Geveke
# 10/25/2022

class Camera():
    import pyrealsense2 as rs
    import numpy as np
    import cv2
    import keyboard
    import random
    import os
    from time import sleep

    def __init__(self, stream=False, save=True, delay=1):
        print('Camera class __init__()')
        if save:
            self.index = 0
            self.sampleName = 'sample_' + ''.join(self.random.choice('0123456789abcdef') for i in range(8))
            self.os.mkdir(self.sampleName)
            self.path = self.os.path.abspath(self.sampleName)
        self.save = save
        self.stream = stream
        self.delay = delay
        
        # Create a pipeline
        pipeline = self.rs.pipeline()

        # Create a config and configure the pipeline to stream different resolutions of color and depth streams
        config = self.rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = self.rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()

        found_rgb = False
        for s in device.sensors:
            if s.get_info(self.rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("Error finding RGB camera")
            exit(0)

        config.enable_stream(self.rs.stream.depth, 640, 480, self.rs.format.z16, 30)
        config.enable_stream(self.rs.stream.color, 640, 480, self.rs.format.bgr8, 30)

        # Start streaming
        profile = pipeline.start(config)

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = self.rs.stream.color
        self.align = self.rs.align(align_to)
        self.pipeline = pipeline
        if stream:
            # Streaming loop
            try:
                while True:
                    # Get frameset of color and depth
                    try:
                        frames = pipeline.wait_for_frames()
                    except:
                        frames = pipeline.wait_for_frames()

                    # Align the depth frame to color frame
                    aligned_frames = align.process(frames)

                    # Get aligned frames
                    aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
                    color_frame = aligned_frames.get_color_frame()

                    # Validate that both frames are valid
                    if not aligned_depth_frame or not color_frame:
                        continue
                    
                    depth_image = self.np.asanyarray(aligned_depth_frame.get_data())        
                    color_image = self.np.asanyarray(color_frame.get_data())

                    # Render images: depth colormap on left and RGB on right
                    depth_colormap = self.cv2.applyColorMap(self.cv2.convertScaleAbs(depth_image, alpha=0.03), self.cv2.COLORMAP_JET)
                    
                    # Export local to class variables
                    self.depth_image = depth_colormap
                    self.color_image = color_image

                    if self.keyboard.is_pressed('c'):
                        print('Capture')
                        self.capture()
                        self.show()
                        self.sleep(0.5)
            finally:
                pipeline.stop()

    def cropImage(self, img):
        croppedImg = img[0:480, 20:610]  # Crop region of interest
        return croppedImg

    def show(self):
        images = self.np.hstack((self.depth_image, self.color_image))
        self.cv2.namedWindow('Align Example', self.cv2.WINDOW_NORMAL)
        self.cv2.imshow('Align Example', images)

        key = self.cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            self.cv2.destroyAllWindows()

    def capture(self, save=False):
        if not self.stream:
            # Get frameset of color and depth
            frames = self.pipeline.wait_for_frames()

            # Align the depth frame to color frame
            aligned_frames = self.align.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
            color_frame = aligned_frames.get_color_frame()

            # Validate that both frames are valid
            if not aligned_depth_frame or not color_frame:
                return None

            depth_image = self.np.asanyarray(aligned_depth_frame.get_data())
            color_image = self.np.asanyarray(color_frame.get_data())

            # Render images: depth colormap on left and RGB on right
            depth_colormap = self.cv2.applyColorMap(self.cv2.convertScaleAbs(depth_image, alpha=0.03),
                                                    self.cv2.COLORMAP_JET)

            # Export local to class variables
            self.depth_image = depth_colormap
            self.color_image = color_image

        cropped_depth = self.cropImage(self.depth_image)
        cropped_color = self.cropImage(self.color_image)

        if save:
            baseName = self.sampleName + '_' + str(self.index)
            imgName = self.os.path.join(self.sampleName, baseName + '_color.jpg')
            self.index += 1

            self.cv2.imwrite(self.os.path.join(self.path, baseName + '_depth.jpg'), cropped_depth)
            self.cv2.imwrite(self.os.path.join(self.path, baseName + '_color.jpg'), cropped_color)
            print('Saved depth and color images')
            return [cropped_color, cropped_depth, imgName]
        else:
            return [cropped_color, cropped_depth]
    def __del__(self):
        print('Deleting camera object')
        self.pipeline.stop()

if __name__ == '__main__':
    obj = Camera(save=True, stream=False)
    obj.capture(save=True)