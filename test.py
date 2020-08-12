from pillcase import *
import sys

def main():
    pc = Pillcase(inputDir)
    pc.show()
    pc.save("output.jpg")
  
argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
