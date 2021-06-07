import shutil
import os


def move_rename_test(from_folder, to_folder, file_name):
    create_folder(to_folder)
    if file_name in from_folder:
        full_final_path = '{}/{}'.format(to_folder, file_name)
        print(file_name)
        print(os.getcwd())
        with open(file_name, 'r') as f_in:
            with open(full_final_path, 'w') as f_out:
                shutil.copyfileobj(f_in, f_out)


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
