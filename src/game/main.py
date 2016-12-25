import sys
from game.field import Field
if __name__ == "__main__":
    if len(sys.argv) != 2 :
        print("please, provide level file")
        exit(1)
    
    field = Field()
    field.load_file(sys.argv[1])
#     field.load_file(sys.argc)