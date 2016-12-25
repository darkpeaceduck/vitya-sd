import sys
from game.field import Field
from game.gfx import GfxDefault
from game.Manager import Manager
if __name__ == "__main__":
    if len(sys.argv) != 2 :
        print("please, provide level file")
        exit(1)
    
    field = Field()
    field.load_file(sys.argv[1])
    gfx = GfxDefault()
#     gfx = None
    mng = Manager(field, gfx)
    mng.start()
    
