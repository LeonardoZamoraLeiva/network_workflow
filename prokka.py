import os
from move_rename import move_rename
from move_rename import create_folder


def prokkafunc(unzipfolder, currentfolder):
    create_folder('prokka')
    a = []
    b = []
    for subdir, dirs, file in os.walk(unzipfolder):
        for name in file:
            if name.endswith('.fna'):
                print(name)
                c = os.path.join(name)
                a.append(c)
                b.append(c[0:-4])
        print(a)

    i = 0
    sizeofList = len(a)
    print(os.getcwd())
    while i < sizeofList:
        output_folder = '{}/{}/'.format(currentfolder, str(b[i]))
        original_file = '{}/{}'.format(unzipfolder, str(a[i]))

        prokka = 'prokka --outdir {} {}'.format(output_folder, original_file)
        os.system(prokka)

        to_folder = '{}/prokka/{}.gbk'.format(os.getcwd(), str(b[i]))
        move_rename(output_folder, to_folder)

        i += 1
