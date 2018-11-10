#import tkinter
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import os
#from screeninfo import get_monitors

class App:
     def __init__(self, window, window_title, video_source=0):
         self.window = window
         self.window.title(window_title)
         #self.window.maxsize()
         #self.window.resizable(False, False)

         self.window.attributes("-fullscreen", True)
         self.video_source = video_source

         # Gets the requested values of the height and width.
         windowWidth = self.window.winfo_screenwidth() #winfo_reqwidth()
         windowHeight = self.window.winfo_screenheight() #winfo_reqheight()
         #for m in get_monitors():
         #     print(str(m))
 
         # open video source (by default this will try to open the computer webcam)
         self.vid = MyVideoCapture(self.video_source)

         # This loads an image to the background (literally)
		 # ==========================================================
		 # This part is necessary to make sure the color is shown correctly 
         self.cv_img = cv2.cvtColor(cv2.imread('recycleShawn.jpg'), cv2.COLOR_BGR2RGB)

         img = PIL.Image.fromarray(self.cv_img)
         imgW, imgH = img.size

         if (imgH > imgW):
            curImg = windowHeight 
         else:
            curImg = windowWidth

         if imgW > curImg or imgH > curImg:
            if imgH > imgW:
               factor = curImg / imgH
            else:
               factor = curImg / imgW
            tn_image = img.resize((int(imgW * factor), int(imgH * factor)))

         self.photo = PIL.ImageTk.PhotoImage(image = tn_image)
         bk_label = tk.Label(window, image=self.photo)
         bk_label.place(x=0,y=0, relwidth=1, relheight=1) # position of background
         bk_label.image = self.photo # need this otherwise image gets destroyed and white space appears. 

         # Create a canvas that can fit the above video source size
         self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
         #self.canvas = tk.Entry(window)
         self.canvas.pack(pady = 50) #pady, padx moves the canvas around

         # Button that lets the user take a snapshot
         self.btn_snapshot=tk.Button(window, text="Snapshot", width=50, height = 2, command=self.snapshot)
         self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)
 
         # Button that lets the user take a print
         self.btn_print=tk.Button(window, text="Print", width=50, height = 2, command=self.print)
         self.btn_print.pack(anchor=tk.CENTER, expand=True)
 
         # After it is called once, the update method will be automatically called every delay milliseconds
         self.delay = 15
         self.update()

         self.window.mainloop()
 
     def snapshot(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
 
         if ret:
             cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
 
     def print(self):
         # print photo ...
         print("Printing ...")

     def update(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()

         if ret:
             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
             self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW) # 0,0 determines the position of video source relative to the box it is in
         self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
		 # manually set resolution 0.5625
         self.vid.set(3, 640)
         self.vid.set(4, 360)

         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

         self.framerate = self.vid.get(cv2.CAP_PROP_FPS)
         print("w:" , self.width , ",h:" , self.height , ", fr:", self.framerate)
 
     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (ret, None)
 
     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()
 
 # Create a window and pass it to the Application object
App(tk.Tk(), "Tkinter and OpenCV")


#os.system("lpr -P 'Brother MFC-8440 USB' photobooth.txt")