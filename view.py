import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time

from authenticator import authenticate


class ViewGUI:
    def __init__(self, window, window_title, video_source_front=0, video_source_side=0):
        self.window = window
        self.window.title(window_title)
        self.video_source_front = video_source_front
        
        # Defining some images.
        self.images = {
            'check' : PIL.Image.open("data/gui_images/check.png").resize((50, 50), PIL.Image.ANTIALIAS),
            'alert' : PIL.Image.open("data/gui_images/alert.png").resize((50, 50), PIL.Image.ANTIALIAS)
        }

        # Defining a program icon.
        icon = tk.PhotoImage(file='data/gui_images/icon.png')
        self.window.tk.call('wm', 'iconphoto', self.window._w, icon)

        # Open video sources.
        self.vid_front = VideoCapture(self.video_source_front)
        #self.vid_side = VideoCapture(self.video_source_side)

        # Create a canvas.
        self.canvas = tk.Canvas(window, width = self.vid_front.width + self.vid_front.width + 50, height = self.vid_front.height + 100)
        self.canvas.pack()

        # Recognition result.
        self.result = None

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret_f, frame_f = self.vid_front.get_frame()

        if ret_f:
            cv2.imwrite("frame_front-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame_f, cv2.COLOR_RGB2BGR))

    def update(self):
        
        # Get frames from the video sources.
        ret_f, frame_f = self.vid_front.get_frame()
        ret_s, frame_s = self.vid_front.get_frame()
        
        # Show the frames in GUI.
        if ret_f:
            self.photo_f = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_f))
            self.canvas.create_image(10, 20, image = self.photo_f, anchor = tk.NW)
        
        if ret_s:
            self.photo_s = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_s))
            self.canvas.create_image(670, 20, image = self.photo_s, anchor = tk.NW)
        
        # Run authenticator with collected photos.
        self.result = authenticate(self.photo_f, self.photo_s)

        # Show authentication image.
        render = PIL.ImageTk.PhotoImage(self.images[self.result['im']])
        img = tk.Label(self.window, image=render)
        img.image = render
        img.place(x=self.vid_front.width - 120, y=self.vid_front.height + 35)
        
        # Show authentication text.
        text = tk.Label(self.window, text=self.result['text'])
        text.pack()
        text.place(x=self.vid_front.width - 60, y=self.vid_front.height + 50)

        # Recursive loop.
        self.window.after(self.delay, self.update)

class VideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()