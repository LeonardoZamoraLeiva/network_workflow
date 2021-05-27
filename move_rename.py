import shutil
import os


def move_rename(from_folder, to_folder):
    for subdir, dirs, files in os.walk(from_folder):
        for file in files:
            if file.endswith('.gbk'):
                print(file)
                print(os.getcwd())
                with open(from_folder+file, 'r') as f_in:
                    with open(to_folder, 'w') as f_out:
                        shutil.copyfileobj(f_in, f_out)


def create_folder(folder):
    mydir = folder
    if not os.path.isdir(mydir):
        os.makedirs(mydir)
        print('Created folder: ', mydir)
    else:
        print(mydir, ' folder already exists')