import os
import shutil
from utils import get_style
from style_change_method import (var_name_style_to_camel_case, var_name_style_to_initcap, 
                                 var_name_style_to_underscore, var_name_style_to_init_underscore, 
                                 var_name_style_to_init_dollar, pointer_to_array, array_to_pointer, 
                                 re_temp, temporary_var, var_init_merge, var_init_pos, init_declaration, 
                                 var_init_split, assign_value, assign_combine, incr_opr_prepost_to_incr_postfix, 
                                 incr_opr_prepost_to_incr_prefix, incr_opr_prepost_to_full_incr, 
                                 incr_opr_prepost_to_separate_incr, typedef, retypedef, dyn_static_mem, 
                                 static_dyn_mem, while_for, for_while, switch_if, ternary, if_spilt, if_combine)

# 2,3,4,12,13,14,15,16,17 need target author
# 18 to cpp
style_mapping = {
    # 1.x 变量名风格转换
    '1.1': 'var_name_style_to_camel_case',      # aaaBbbCcc
    '1.2': 'var_name_style_to_initcap',         # AaaBbbCcc
    '1.3': 'var_name_style_to_underscore',      # aaa_bbb_ccc
    '1.4': 'var_name_style_to_init_underscore', # _aaa_bbb_ccc
    '1.5': 'var_name_style_to_init_dollar',     # $aaa_bbb_ccc
    # 5.1 指针 <-> 数组
    '5.1': 'pointer_to_array',                  # *(a+1)
    '5.2': 'array_to_pointer',                  # a[1]
    # 6.x 变量名申明的位置放在(6.1最前面/6.2使用该变量名的前一行)
    '6.1': 're_temp',                           # int a;\n  for(;;;);\n  a++;
    '6.2': 'temporary_var',                     # for(;;;);\n  int a;\n  a++;
    # 7.x 变量名声明与赋值(7.1合并/7.2分开)
    '7.1': 'var_init_merge',                    # int a = 0;
    '7.2': 'var_init_pos',                      # int a;\n  a = 0;
    # 8.x 多个变量名声明(8.1合并/8.2分离)
    '8.1': 'init_declaration',                  # int a = 0, b = 0;
    '8.2': 'var_init_split',                    # int a = 0;\n  int b = 0;
    # 9.x 在数据集中都较为稀少，conv -> 0%
    '9.1': 'assign_value',  
    '9.2': 'assign_combine',
    # 10.x 循环中的+1写法
    '10.1': 'incr_opr_prepost_to_incr_postfix', # i++ 
    '10.2': 'incr_opr_prepost_to_incr_prefix',  # ++i
    '10.3': 'incr_opr_prepost_to_full_incr',    # i=i+1
    '10.4': 'incr_opr_prepost_to_separate_incr',# i+=1
    # 19.2 静态分配内存变为动态
    '19.2': 'static_dyn_mem',                   # int *a = (int *)malloc(sizeof(int) * (10));
    # 20.x while <-> for
    '20.1': 'while_for',                        # for
    '20.2': 'for_while',                        # while
    # if条件(22.1分离/22.2合并)
    '22.1': 'if_spilt',                         # if (a) if (b)
    '22.2': 'if_combine'                        # if (a && b)
}       

def change_style(code, choice, file_type='c'):
    converted_styles = []
    for idx in choice:
        if idx in style_mapping:
            converted_styles.append(style_mapping[idx])
    temp_dir = 'temp_' + '_'.join(choice)
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    code_file = temp_dir + '/code.' + file_type
    copy_file = temp_dir + '/copy.' + file_type
    xml_file = temp_dir + '/xml'
    code_change_file = temp_dir + '/change' + file_type
    with open(code_file,'w') as f:
        f.write(code)
    os.system('clang-format -i -style="{IndentWidth: 4}" '+ code_file)  # use clang-format
    get_style.srcml_program_xml(code_file, xml_file)
    program_style = get_style.get_style(xml_file + '.xml', file_type)
    shutil.copy(code_file, copy_file)
    for i in range(len(converted_styles)):
        get_style.srcml_program_xml(copy_file, xml_file)
        eval(converted_styles[i]).program_transform_save_div(xml_file, './')
        get_style.srcml_xml_program(xml_file + '.xml', code_change_file)
        shutil.move(code_change_file, copy_file)
    os.system('clang-format -i -style="{IndentWidth: 4}" '+ copy_file)  # use clang-format
    with open(code_file, 'r') as f:
        orig_code = f.read()
    with open(copy_file, 'r') as f:
        new_code = f.read()
    succ = ( new_code.replace(' ','').replace('\n','') != code.replace(' ','').replace('\n','') )
    shutil.rmtree(temp_dir)
    return orig_code, new_code, succ

if __name__ == '__main__':
    with open('test.c', 'r') as f:
        code = f.read()
    orig_code, new_code, succ = change_style(code, ['22.1','1.4','20.2'], file_type='c')
    print(orig_code)
    print(new_code)
    print(succ)
