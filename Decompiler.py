from unpyc3 import decompile, dec_module
import io
import os
import sys

PATH_DIR = "./"

if not os.path.exists(PATH_DIR):
    sys.exit("\n\nError! Source Path Not Found!\nTry To Change the PATH_DIR inside this file.\n")


if not os.path.exists("./decompiled/"): os.makedirs("./decompiled/")
for root, dirs, files in os.walk(PATH_DIR):
    path = root.split('/')
    slash = "";
    if(len(path) > 1):
        slash = "/"
    for file in files:
        if file.endswith(".pyo"):
            if not os.path.exists("./decompiled/"+root+slash):
                os.makedirs("./decompiled/"+root+slash)
            fileName = root+slash+file
            f1 = open("./decompiled/" + fileName.replace(".pyo",".py"),"w+")
            try:
                result = decompile(fileName)
                print(result.__str__().encode('unicode_escape', 'strict').decode().replace('\\n', '\n'), file=f1)
                print(root + slash + file + ' --> DECOMPILED!')
                f1.close()
            except UnicodeEncodeError as error:   
                print('Error when decompiling: ' + fileName)
                print(sys.exc_info())
                continue
            continue
        else:
            continue
