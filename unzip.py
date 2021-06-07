import os
import shutil
import gzip
from move_rename import create_folder


def unzipfunc(from_folder, to_folder):
    create_folder('unzip')
    for direct, subdir, files in os.walk(from_folder):
        for name in files:
            full_path = '{}/{}'.format(from_folder, name)
            print(full_path)
            final_path = to_folder
            if full_path.endswith(".gz"):
                try:
                    with gzip.open(full_path, 'rb') as f_in:

                        with open(to_folder + '/' + name[0:-3], 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)

                        f_in.close()
                        f_out.close()
                        print('File {} will be uncompress to {} under the name of {}'.format(full_path, final_path,
                                                                                             f_out.name))
                except:
                    print("Can't unzip the file {}".format(full_path))
