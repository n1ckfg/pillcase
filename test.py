from pillcase import *
import sys

def main():
    pc = Pillcase(url=inputDir)   

    pc.setFill(0,127,255,127)
    pc.setStroke(255,0,0,127)
    pc.setStrokeWeight(10)

    pc.background(11, 50, 0, 127)

    points = [ 0, 0, 100, 100, 200, 100, 0, 0 ]
    pc.polygon(points)
    pc.line(0, 0, pc.width, pc.height)
    pc.point(110, 50)

    pc.setStrokeWeight(4)
    pc.setStroke(255,0,255,50)
    pc.ellipse(320,340,50,100)
    
    pc.rect(400, 400, 50, 50)

    img = pc.get(0,0,pc.width,pc.height)
    img = pc.resize(img, 320,240)
    pc.crop(0,0,640,240)
    pc.image(img, 0, 0)
    pc.image(img, 320, 0)
    pc.image(img, 50, 50, 100, 100)

    pc.show()
    pc.save("output.png")
  
argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
