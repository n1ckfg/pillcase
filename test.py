from pillcase import *
import sys

def main():
    pc = Pillcase(inputDir)
    
    points = [ 0, 0, 100, 100, 200, 100, 0, 0 ]
    pc.setFill(0,127,255)
    pc.setStroke(255,0,0)
    pc.polygon(points)
    pc.setStrokeWeight(3)
    pc.line([ 0, 0, pc.width, pc.height ])
    pc.point(110, 0)
    
    pc.show()
    pc.save("output.jpg")
  
argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
