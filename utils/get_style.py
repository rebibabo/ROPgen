# -*- coding: utf-8 -*-
# author:yejunyao
# datetime:2022/10/27 15:19
"""

    Instructions:
    The original program of each author is transformed into an XML file,
    and the proportion of each type of each author is calculated

    Input:'./program_file/target_author_file':target author program
    Output:'./author_style':author style
            './xml_file':author program's xml file

    Steps:
    1. convert source program to XML file
    2. get author's style
"""
import os
import subprocess
import re
import sys
from tqdm import tqdm

from utils import tools
from get_transform import (transform_1, transform_2, transform_3, transform_4, transform_5, transform_6, transform_7,
                           transform_8, transform_9,
                           transform_10, transform_11, transform_12, transform_13, transform_14, transform_15,
                           transform_16, transform_17, transform_18, transform_19,
                           transform_20, transform_21, transform_22, transform_23)

cur_path = os.path.abspath('src')
up_path = os.path.dirname(cur_path)
sys.path.append(up_path)
sys.path.append(cur_path)

flag = True  # indicates whether the shell command runs successfully
# file_type = 'c'  # program's style c++/java/c


# express shell command
def cmd(command):
    """
    执行shell
    """
    global flag
    flag = True
    # input()
    subp = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    subp.wait(10)
    if subp.poll() == 0:
        flag = True
    else:
        flag = False
        

#
def program_to_xml(pre_file, xml_file, file_type='c'):
    """
    convert original program to xml file
    这个限制了文件夹的层数，只能有两层，第一层是类别，第二层是程序
    """
    tools.create_empty_dir(xml_file)

    # global file_type

    total_files = 0
    for sub_dir in os.listdir(pre_file):
        files_path = os.path.join(pre_file, sub_dir)
        total_files += len(os.listdir(files_path))
    progress_bar = tqdm(total=total_files, desc='Processing', unit='file')
    for sub_dir in os.listdir(pre_file):
        files_path = os.path.join(pre_file, sub_dir)
        # create the corresponding XML file directory
        if not os.path.exists(os.path.join(xml_file, sub_dir)):
            os.mkdir(os.path.join(xml_file, sub_dir))
        for file in os.listdir(files_path):
            # get program name (without suffix) ,如果是txt文件则默认c语言
            if file.split('.')[-1] == 'java': file_type = 'java'
            if file.split('.')[-1] == 'cpp': file_type = 'cpp'
            name = re.findall(r'(.+?)\.', file)\
            # 如果os.path.join(xml_file, sub_dir, name[0])+'.xml'文件存在，则跳过
            if os.path.exists(os.path.join(xml_file, sub_dir, name[0]) + '.xml'):
                continue
            srcml_program_xml(os.path.join(files_path, file), os.path.join(xml_file, sub_dir, name[0]))
            if flag is False:
                continue
            progress_bar.update(1)
    progress_bar.close()


#
def srcml_program_xml(pre_path, xml_path):
    """
        convert program to xml
    """
    
    str_com = 'srcml \"' + pre_path + '\" -o \"' + xml_path + '.xml\" --position --src-encoding UTF-8'
    cmd(str_com)


#
def srcml_xml_program(pre_path, xml_path):
    """
        convert xml to program
    """
    str_com = "srcml \"" + pre_path + '\" -o \"' + xml_path + "\" --src-encoding UTF-8"
    cmd(str_com)


# calculate every author's style
def get_style(xml_file_path, file_type='c'):
    # global file_type
    style_list = []
    for i in [1, 5, 6, 7, 8, 9, 10, 11, 19, 20, 21, 22]:
    # for i in range(1, 24):
        transform_name = 'transform_' + str(i)
        doc = eval(transform_name)
        style_list.append(doc.get_program_style(xml_file_path, file_type))
    return style_list


# Calculate the style proportion of each author
def calculate_proportion(style_list, auth_nums):
    new_style_list = style_list[0]
    for index in range(len(style_list)):
        if index == 0: continue
        one_style_list = style_list[index]
        for i in range(1, 24):
            if i == 23:
                for j in range(0, 2):
                    new_style_list[i]['23'][j] += one_style_list[i]['23'][j]
                continue
            for key in one_style_list[i]:
                new_style_list[i][key] += one_style_list[i][key]
    for i in range(1, 24):
        if i == 23:
            for j in range(0, 2):
                new_style_list[i]['23'][j] = round((new_style_list[i]['23'][j] / auth_nums), 1)
            continue
        if i == 4:
            if new_style_list[i]['4.1'] > 0:
                new_style_list[i]['4.1'] = 100.0
                continue
        if i == 11:
            if new_style_list[i]['11.1'] > 0:
                new_style_list[i]['11.1'] = 100.0
                continue
        if i == 12:
            if new_style_list[i]['12.1'] > 0:
                new_style_list[i]['12.1'] = 100.0
                continue
        sum1 = sum(new_style_list[i].values())
        if sum1 == 0: continue
        for key in new_style_list[i]:
            new_style_list[i][key] = round((new_style_list[i][key] / sum1) * 100, 1)
    return new_style_list


# get all author's style and store them to './author_style'
def get_auth_style(xml_file, author_style_path):
    tools.create_empty_dir(author_style_path)
    print('----------Start getting target author style----------')
    for sub_dir in os.listdir(xml_file):
        # create author style file
        f = open(os.path.join(author_style_path, sub_dir + '.txt'), 'w')
        files_path = os.path.join(xml_file, sub_dir)
        style_list = []
        for file in os.listdir(files_path):
            print("----------------")
            print("Author " + sub_dir + " proportion of  program " + file + " : ")
            # traverse each XML file
            # get the path of each XML file
            xml_file_path = os.path.join(files_path, file)
            # calculate every author's style
            one_style_list = get_style(xml_file_path)
            style_list.append(one_style_list)
            # Calculate the style proportion of each author
        new_style_list = calculate_proportion(style_list, len(os.listdir(files_path)))
        for elem in new_style_list[1:]:
            f.write(str(elem) + '\n')
        f.close()
    print('----------Complete %d authors----------' % (len(os.listdir(xml_file))))


def main():
    # all untransformed original program
    pre_file = "datasets/target_author_file"
    os.makedirs(pre_file, exist_ok=True)

    # store XML file of all source programs
    xml_file = "style/target_author_xml/"
    os.makedirs(xml_file, exist_ok=True)

    # store target author style
    author_style_path = 'style/target_author_style/'
    # convert source program to XML file
    os.makedirs(author_style_path, exist_ok=True)
    program_to_xml(pre_file, xml_file)
    # get all author's style and store them to './author_style'
    get_auth_style(xml_file, author_style_path)


# the project's input port
if __name__ == '__main__':
    main()
