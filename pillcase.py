import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

class Pillcase(object):

    def __init__(self, width=None, height=None, url=None):
        if not url:
            self.width = width
            self.height = height
            self.new(self.width, self.height)
        else:
            self.load(url)

    def new(self, _width, _height):
        self.image = self.create(_width, _height)
        self.init()

    def load(self, _url):
        self.image = Image.open(_url)
        self.init()

    def create(self, _width, _height):
        return Image.new("RGB", (_width, _height))

    def init(self):
        self.pixels = self.image.load()
        self.width = self.image.size[0]
        self.height = self.image.size[1]

        # https://stackoverflow.com/questions/359706/how-do-you-draw-transparent-polygons-with-python
        self.canvas = ImageDraw.Draw(self.image, "RGBA")

        self.fill = self.setFill((255,255,255))
        self.stroke = self.setFill((0,0,0))
        self.strokeWeight = 1
        print (str(self.image.format) + " " + str(self.image.size) + " " + str(self.image.mode))

    def show(self):
        self.image.show()

    def blend(self, _image1, _image2, _alpha):
        return Image.blend(_image1.convert("RGBA"), _image2.convert("RGBA"), alpha=_alpha/255.0)

    def save(self, _url, _alpha=False):
        if (_alpha == True):
            self.image.convert("RGBA").save(_url)
        else:
            self.image.convert("RGB").save(_url)

    def crop(self, _x1, _y1, _x2, _y2):
        box = (_x1, _y1, _x2, _y2)
        region = self.image.crop(box)
        #region = region.transpose(Image.ROTATE_180)
        self.new(_x2-_x1, _y2-_y1)
        self.image.paste(region, box)

    def background(self, _r, _g=None, _b=None, _a=None):
        color = self.createColor(_r, _g, _b, _a)
        points = [ 0, 0, self.width, self.height ]
        self.canvas.rectangle(points, fill=color, outline=None)

    def setFill(self, _r, _g=None, _b=None, _a=None):
        self.fill = self.createColor(_r, _g, _b, _a)

    def setStroke(self, _r, _g=None, _b=None, _a=None):
        self.stroke = self.createColor(_r, _g, _b, _a)

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

    # https://pillow.readthedocs.io/en/5.1.x/reference/ImageDraw.html#methods
    def polygon(self, _points):
        self.canvas.polygon(_points, fill=self.fill, outline=self.stroke)
        if (self.strokeWeight > 1):
            self.polyline(_points)

    def getBounds(self, _x, _y, _w, _h):
        _x1 = _x - _w/2
        _y1 = _y - _h/2
        _x2 = _x + _w/2
        _y2 = _y + _h/2
        return [ _x1, _y1, _x2, _y2 ]

    def traceBounds(self, _x, _y, _w, _h):
        _x1, _y1, _x2, _y2 = self.getBounds(_x, _y, _w, _h)
        return [ _x1, _y1, _x2, _y1, _x2, _y2, _x1, _y2, _x1, _y1 ]

    def ellipse(self, _x, _y, _w, _h):
        self.canvas.ellipse(self.getBounds(_x, _y, _w, _h), fill=self.fill, outline=self.stroke, width=self.strokeWeight)

    def rect(self, _x, _y, _w, _h):
        self.canvas.rectangle(self.getBounds(_x, _y, _w, _h), fill=self.fill, outline=self.stroke, width=self.strokeWeight)       	

    def line(self, _x1, _y1, _x2, _y2):
        self.canvas.line([_x1, _y1, _x2, _y2], fill=self.stroke, width=self.strokeWeight)

    def polyline(self, _points):
        self.canvas.line(_points, fill=self.stroke, width=self.strokeWeight)

    def point(self, _x, _y):
        if (self.strokeWeight > 1):
            self.canvas.ellipse(self.getBounds(_x, _y, self.strokeWeight, self.strokeWeight), fill=self.stroke, outline=None)
        else:
            self.canvas.point([ _x, _y ], fill=self.stroke)


