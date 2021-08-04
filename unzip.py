import os
import shutil
import gzip
from move_rename import create_folder


def unzipfunc(from_folder, to_folder,report_dict):
    create_folder('unzip_vb1')
    for direct, subdir, files in os.walk(from_folder):
        for name in files:
            #full_path = '{}/{}'.format(os.getcwd(),name)
            full_path = '{}/{}'.format(direct, name)
            print(full_path)
            strain_name = direct.split('/')
            report_dict['strain_name'].append(strain_name[-1])
            report_dict['Bin Id'].append(name[0:-7])
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
