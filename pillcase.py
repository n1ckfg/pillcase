import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

import argparse
import glob
import os


class Batcher(object):
    
    def __init__(self, filetype1="jpg", filetype2="png"):
        parser = argparse.ArgumentParser()
        parser.add_argument("--input_dir", help="path to folder containing images")
        parser.add_argument("--output_dir", required=True, help="where to put output files")
        #parser.add_argument("--model", default=None, help="path to model directory")
        a = parser.parse_args()

        if a.input_dir is None or not os.path.exists(a.input_dir):
            raise Exception("Input_dir does not exist.")

        self.input_paths = glob.glob(os.path.join(a.input_dir, "*."+filetype1))

        if len(self.input_paths) == 0:
            self.input_paths = glob.glob(os.path.join(a.input_dir, "*."+filetype2))

        if len(self.input_paths) == 0:
            raise Exception("Input_dir contains no image files.")

        self.input_paths.sort()

        self.output_path = a.output_dir
        if not os.path.exists(a.output_dir):
            os.makedirs(a.output_dir)


class Pillcase(object):

    def __init__(self, width=None, height=None, url=None):
        if not url:
            self.width = width
            self.height = height
            self.canvas = self.create(self.width, self.height)
        else:
            self.canvas = self.load(url)
        self.setup()

    def setup(self):
        self.pixels = self.canvas.load()
        self.width = self.canvas.size[0]
        self.height = self.canvas.size[1]

        # https://stackoverflow.com/questions/359706/how-do-you-draw-transparent-polygons-with-python
        try:
            self.draw = ImageDraw.Draw(self.canvas, "RGBA")
        except:
            print("Source image is not RGBA, drawing will not be possible.")

        self.fill = self.setFill(255)
        self.stroke = self.setStroke(0)
        self.strokeWeight = self.setStrokeWeight(1)
        print (str(self.canvas.format) + " " + str(self.canvas.size) + " " + str(self.canvas.mode))

    def load(self, _url):
        return Image.open(_url)

    def create(self, _width, _height):
        return Image.new("RGB", (_width, _height))

    def new(self, _width, _height):
        self.canvas = self.create(_width, _height)
        self.setup()

    def show(self):
        self.canvas.show()

    def save(self, _url="output.png", _alpha=False):
        if (_alpha == True):
            self.canvas.convert("RGBA").save(_url)
        else:
            self.canvas.convert("RGB").save(_url)

    def crop(self, _x1, _y1, _x2, _y2):
        img = self.get(self.canvas, _x1, _y1, _x2, _y2)
        self.new(_x2-_x1, _y2-_y1)
        self.image(img, 0, 0)

    # IMAGES
    def blend(self, _image1, _image2, _alpha):
        return Image.blend(_image1.convert("RGBA"), _image2.convert("RGBA"), alpha=_alpha/255.0)

    def get(self, img, _x1, _y1, _x2, _y2):
        box = (_x1, _y1, _x2, _y2)
        return img.crop(box)

    def resize(self, img, w, h):
        return img.resize((w, h), Image.ANTIALIAS)

    def rotate(self, img, angle):
        # https://pythonexamples.org/python-pillow-rotate-image-90-180-270-degrees/
        return img.rotate(angle, expand=True, resample=3, fillcolor=(0,0,0,0))

    def image(self, img, _x1, _y1, _x2=None, _y2=None):
        if (_x2 != None and _y2 != None):
            img = img.resize((_x2-_x1, _y2-_y1), Image.ANTIALIAS)
        self.canvas.paste(img, (_x1, _y1))

    def squareCrop(self, img, val=None):
        x = 0
        y = 0
        w = img.size[0]
        h = img.size[1]
        if (w > h):
            x = (w-h)/2
            w = h
        elif (w < h):
            y = (h-w)/2
            h = w
        
        if not val:
            return self.get(img, x, y, w, h)
        else:
            return self.resize(self.get(img, x, y, w, h), val, val)

    def colorCrop(self, img, bgcolor):
        w = img.size[0]
        h = img.size[1]
        pixels = img.load()
        allX = []
        allY = []
        bgcolor = self.createColor(bgcolor)

        for y in range(0, h):
            for x in range(0, w):
                c = self.getPixel(pixels, x, y)
                if (c != bgcolor):
                    allX.append(x)
                    allY.append(y)

        allX.sort()
        allY.sort()

        minX = allX[0]
        minY = allY[0]
        maxX = allX[len(allX)-1] - minX
        maxY = allY[len(allY)-1] - minY

        return self.get(img, minX, minY, maxX, maxY)   

    def getPixel(self, pixels, x, y):
        r, g, b = pixels[x, y]
        return self.createColor((r, g, b))

    # DRAWING
    def background(self, _r, _g=None, _b=None, _a=None):
        color = self.createColor(_r, _g, _b, _a)
        points = [ 0, 0, self.width, self.height ]
        self.draw.rectangle(points, fill=color, outline=None)

    def setFill(self, _r, _g=None, _b=None, _a=None):
        self.fill = self.createColor(_r, _g, _b, _a)
        return self.fill

    def setStroke(self, _r, _g=None, _b=None, _a=None):
        self.stroke = self.createColor(_r, _g, _b, _a)
        return self.stroke

    def createColor(self, _r, _g=None, _b=None, _a=None):
        if _g == None and _a == None:
            return (_r, _r, _r, 255)
        elif _g == None and _a != None:
            return (_r, _r, _r, _a)
        elif _g != None and _a == None:
            return (_r, _g, _b, 255)
        elif (_g != None and _a != None):
            return (_r, _g, _b, _a)

    def noStroke(self):
        self.stroke = None

    def noFill(self):
        self.fill = None

    def setStrokeWeight(self, _val):
        self.strokeWeight = _val
        if (self.strokeWeight <= 0):
            noStroke()
        return self.strokeWeight

    # https://pillow.readthedocs.io/en/5.1.x/reference/ImageDraw.html#methods
    def polygon(self, _points):
        self.draw.polygon(_points, fill=self.fill, outline=self.stroke)
        if (self.strokeWeight > 1):
            self.polyline(_points)

    def ellipse(self, _x, _y, _w, _h):
        self.draw.ellipse(self.getBounds(_x, _y, _w, _h), fill=self.fill, outline=self.stroke, width=self.strokeWeight)

    def rect(self, _x, _y, _w, _h):
        self.draw.rectangle(self.getBounds(_x, _y, _w, _h), fill=self.fill, outline=self.stroke, width=self.strokeWeight)           

    def line(self, _x1, _y1, _x2, _y2):
        self.draw.line([_x1, _y1, _x2, _y2], fill=self.stroke, width=self.strokeWeight)

    def polyline(self, _points):
        self.draw.line(_points, fill=self.stroke, width=self.strokeWeight)

    def point(self, _x, _y):
        if (self.strokeWeight > 1):
            self.draw.ellipse(self.getBounds(_x, _y, self.strokeWeight, self.strokeWeight), fill=self.stroke, outline=None)
        else:
            self.draw.point([ _x, _y ], fill=self.stroke)

    # UTILITIES
    def getBounds(self, _x, _y, _w, _h):
        _x1 = _x - _w/2
        _y1 = _y - _h/2
        _x2 = _x + _w/2
        _y2 = _y + _h/2
        return [ _x1, _y1, _x2, _y2 ]

    def getBorder(self, _x, _y, _w, _h):
        _x1, _y1, _x2, _y2 = self.getBounds(_x, _y, _w, _h)
        return [ _x1, _y1, _x2, _y1, _x2, _y2, _x1, _y2, _x1, _y1 ]

    def constrain(self, _val, _min, _max):
        if (_val < _min):
            _val = _min
        elif (_val > _max):
            _val = _max
        return _val
