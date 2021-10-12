import multiprocessing as mp
from PIL import Image
from functools import partial
import numpy 
import math
import json

class Set_Gif:
    def __init__(self, w, h, maxIter, thres, inc_begin, inc_scale_by, 
                zoom=1, d_color="white", d_X=0, d_Y=0, framerate=20):
        self.w = w
        self.h = h
        self.zoom = zoom
        self.d_color = d_color
        self.d_X = d_X
        self.d_Y = d_Y
        self.maxIter = maxIter
        self.thres = thres
        self.inc_begin = inc_begin
        self.inc_scale_by = inc_scale_by
        #self.process_ct = mp.cpu_count
        self.framerate = framerate

    def julia_gif(self, x_0, x_1, x_step, c_0, filename):
        gif = []
        c_range = []

        for x in numpy.arange(x_0, x_1, x_step):
            c = c_0 * (complex(math.cos(x), math.sin(x)))
            c_range.append(c)

        #process_ct  = mp.cpu_count
        next_frame = partial(self.draw_complex_frame, type='julia')
        subprocesses = mp.Pool(processes=10)
        gif = subprocesses.map(next_frame, c_range)

        gif[0].save(filename, format='GIF', append_images=gif[1:],
                        save_all=True, duration=self.framerate, loop=0)

    

    def mandelbrot_frame(self):
        return self.draw_complex_frame(0, 'mandelbrot')

    def julia_frame(self, c):
        return self.draw_complex_frame(c, 'julia')

    def draw_complex_frame(self, c, type):
        # creating new frame in RGB mode (Pillow image)
        frame = Image.new("RGB", (self.w, self.h), self.d_color) 
    
        # Allocating the storage for the image and loading the pixel data. 
        pix = frame.load()  

        for x in range(self.w): 
            for y in range(self.h): 
                z = complex( 2.5 * (x - self.w/2) / (0.5 * self.zoom * self.w) + self.d_X, 
                             1.5 * (y - self.h/2) / (0.5 * self.zoom * self.h) + self.d_Y)
                if type == 'julia':
                    i = self.iterate_complex_func(z, c)
                elif type == 'mandelbrot':   
                    i = self.iterate_complex_func(c, z)
                # convert value to RGB (3 bytes)
                #pix[x,y] = (i << 48) + (i << 21) + i*48
                pix[x,y] = (i << 5) + (i << 33) + i*176

               
        return frame
    

    def iterate_complex_func(self, z, c):
        i = self.inc_begin 

        while i != self.maxIter: 
            if abs(z) > self.thres:
                return i;
            z = z*z + c
            i+=self.inc_scale_by

        return 0;

if __name__ == "__main__":
    Frame1 = Set_Gif(3840,  2160, 255,  4,  0,  1)
    Frame1.julia_gif(0, 2*math.pi, .01*math.pi, .7885, './julia_sets.gif')
