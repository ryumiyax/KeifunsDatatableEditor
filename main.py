import sys
from src import program

if __name__ == "__main__":
    folder_path = ""
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]

    ui = program.Program(folder_path)
    ui.run()