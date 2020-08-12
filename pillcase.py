import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

class Pillcase(object):

    def __init__(self, _url=None, _height=None, _width=None):
        self.image = None
        self.draw = None
        if not _url:
            self.width = _width
            self.height = _height
            self.new()
        else:
            self.load(_url)

    def new(self):
        self.image = Image.new("RGB", (self.width, self.height))
        self.init()

    def load(self, _url):
        self.image = Image.open(_url)
        self.init()

    def init(self):
        self.draw = ImageDraw.Draw(self.image)
        self.pixels = self.image.load()
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        print (str(self.image.format) + " " + str(self.image.size) + " " + str(self.image.mode))

    def show(self):
        self.image.show()

    def save(self, _url):
        self.image.save(_url)

    def crop(self, _x1, _y1, _x2, _y2):
        box = (_x1, _y1, _x2, _y2)
        self.image = self.image.crop(box)
        #region = region.transpose(Image.ROTATE_180)
        #self.image.paste(region, box)

    def polygon(self, _points, _fill=(127, 127, 127), _stroke=(255,255,255)):
        self.draw.polygon(_points, _fill, _stroke)




