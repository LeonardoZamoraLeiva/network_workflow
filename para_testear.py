import os

current = '{}/{}'.format(os.getcwd(), 'name_change')
for file in os.listdir(current):
    file_name_init = file.split('.')[0]
    file_name = '{}-{}'.format(file_name_init.split('_')[0],file_name_init.split('_')[1])
    with open('{}/{}'.format(current, file)) as f:
        count = 0
        lines = f.readlines()
        for i in range(len(lines)):
            if '>' in lines[i]:
                new_line = '>{}-ctg{} {}'.format(file_name, count, lines[i][1::])
                print('Changing header of {}\nOriginal header: {}\nNew header: {}'.format(file, lines[i],new_line))
                count += 1
                lines[i] = new_line

    with open('{}/{}'.format(current, file), "w") as f:
        f.writelines(lines)
