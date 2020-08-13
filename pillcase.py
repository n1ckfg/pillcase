import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

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
        self.draw = ImageDraw.Draw(self.canvas, "RGBA")

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

    def save(self, _url, _alpha=False):
        if (_alpha == True):
            self.canvas.convert("RGBA").save(_url)
        else:
            self.canvas.convert("RGB").save(_url)

    # IMAGES
    def blend(self, _image1, _image2, _alpha):
        return Image.blend(_image1.convert("RGBA"), _image2.convert("RGBA"), alpha=_alpha/255.0)

    def crop(self, _x1, _y1, _x2, _y2):
        box = (_x1, _y1, _x2, _y2)
        region = self.canvas.crop(box)
        #region = region.transpose(Image.ROTATE_180)
        self.canvas = self.create(_x2-_x1, _y2-_y1)
        self.canvas.paste(region, box=box)

    def get(self, _x1, _y1, _x2, _y2):
        box = (_x1, _y1, _x2, _y2)
        return self.canvas.crop(box)

    def resize(self, img, w, h):
        return img.resize((w, h), Image.ANTIALIAS)

    def rotate(self, img, angle):
    	# https://pythonexamples.org/python-pillow-rotate-image-90-180-270-degrees/
    	return img.rotate(angle, expand=True, resample=3, fillcolor=(0,0,0,0))

    def image(self, img, _x1, _y1, _x2=None, _y2=None):
        if (_x2 != None and _y2 != None):
            img = img.resize((_x2-_x1, _y2-_y1), Image.ANTIALIAS)
        self.canvas.paste(img, (_x1, _y1))

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

