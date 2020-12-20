from pillcase import *

def main():
    batcher = Batcher()

    for i in range(0, len(batcher.input_paths)):
        print("Reading from : " + batcher.input_paths[i])

        pc = Pillcase(url=batcher.input_paths[i])   

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

        img = pc.get(pc.canvas,0,0,pc.width,pc.height)
        img = pc.resize(img, 320,240)
        pc.crop(0,0,640,240)
        pc.image(img, 0, 0)
        pc.image(img, 320, 0)
        pc.image(img, 50, 50, 100, 100)

        pc.show()
        pc.save(os.path.join(batcher.output_path, "output" + str(i) + ".png"))

        print("Writing file " + str(i+1) + "/" + str(len(batcher.input_paths)) + " to: " + batcher.output_path)

main()
