from pillcase import *

def main():
    batcher = Batcher()

    for i in range(0, len(batcher.input_paths)):
        print("Reading from : " + batcher.input_paths[i])

        pc = Pillcase(url=batcher.input_paths[i])
        img = pc.get(pc.canvas,0,0,pc.width,pc.height)

        if (pc.width > pc.height):
            img = pc.resize(img, pc.height, pc.height)
            pc.crop(0, 0, img.width, img.height)
            pc.image(img, 0, 0)
        elif (pc.height > pc.width):
            img = pc.resize(img, pc.width, pc.width)
            pc.crop(0, 0, img.width, img.height)
            pc.image(img, 0, 0)


        #pc.show()
        pc.save(os.path.join(batcher.output_path, "output" + str(i) + ".png"))

        print("Writing file " + str(i+1) + "/" + str(len(batcher.input_paths)) + " to: " + batcher.output_path)

main()
