import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

class Pillcase(object):

    def __init__(self, _url=None, _height=None, _width=None):
        if not _url:
            self.width = _width
            self.height = _height
            self.new(self.width, self.height)
        else:
            self.load(_url)

    def new(self, _width, _height):
        self.image = Image.new("RGB", (_width, _height))
        self.init()

    def load(self, _url):
        self.image = Image.open(_url)
        self.init()

    def init(self):
        self.draw = ImageDraw.Draw(self.image)
        self.pixels = self.image.load()
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.fill = self.setFill((255,255,255))
        self.stroke = self.setFill((0,0,0))
        self.strokeWeight = 1
        print (str(self.image.format) + " " + str(self.image.size) + " " + str(self.image.mode))

    def show(self):
        self.image.show()

    def save(self, _url):
        self.image.save(_url)

    def crop(self, _x1, _y1, _x2, _y2):
        box = (_x1, _y1, _x2, _y2)
        region = self.image.crop(box)
        #region = region.transpose(Image.ROTATE_180)
        self.new(_x2-_x1, _y2-_y1)
        self.image.paste(region, box)

    def background(self, _r, _g, _b):
        color = (_r, _g, _b)
        points = [ (0, 0), (self.width, 0), (self.width, self.height), (0, self.height), (0, 0) ]
        self.draw.polygon(points, fill=color, outline=color)

    def setFill(self, _r, _g=None, _b=None, _a=None):
        self.fill = self.setColor(_r, _g, _b, _a)

    def setStroke(self, _r, _g=None, _b=None, _a=None):
        self.stroke = self.setColor(_r, _g, _b, _a)

    def setColor(self, _r, _g=None, _b=None, _a=None):
        if _g == None and _a == None:
            return (_r, _r, _r, 255)
        elif _g == None and _a != None:
            return (_r, _r, _r, _a)
        elif _g != None and _a == None:
            return (_r, _g, _b, 255)
        else:
            return (_r, _g, _b, _a)

    def noStroke(self):
        self.stroke = None

    def noFill(self):
        self.fill = None

    def setStrokeWeight(self, _val):
        self.strokeWeight = _val

    # https://pillow.readthedocs.io/en/5.1.x/reference/ImageDraw.html#methods
    def polygon(self, _points):
        self.draw.polygon(_points, fill=self.fill, outline=self.stroke)

    def ellipse(self, _x1, _y1, _x2, _y2):
        self.draw.ellipse([ _x1, _y1, _x2, _y2 ], fill=self.fill, outline=self.stroke)

    def rectangle(self, _x1, _y1, _x2, _y2):
        self.draw.rectangle([ _x1, _y1, _x2, _y2 ], fill=self.fill, outline=self.stroke)

    def line(self, _points):
        self.draw.line(_points, fill=self.stroke, width=self.strokeWeight)

    def point(self, _x1, _y1):
        self.draw.point([ _x1, _y1 ], fill=self.stroke)


