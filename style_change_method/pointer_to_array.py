"""

pointer -> array

"""
import sys
import os
from lxml import etree

ns = {'src': 'http://www.srcML.org/srcML/src',
      'cpp': 'http://www.srcML.org/srcML/cpp',
      'pos': 'http://www.srcML.org/srcML/position'}
doc = None


# parsing XML file into tree
def init_parse(file):
    global doc
    parser = etree.XMLParser(huge_tree=True)
    doc = etree.parse(file, parser)
    e = etree.XPathEvaluator(doc)
    for k, v in ns.items():
        e.register_namespace(k, v)
    return e


# get the label 'expr'
def get_expr(e):
    return e('//src:expr')


# save tree to file
def save_tree_to_file(tree, file):
    with open(file, 'w') as f:
        f.write(etree.tostring(tree).decode('utf8'))


# change the pointer '*(a+i)' to the array 'a[i]' or change the pointer '*(*(a+i)+j)' to the array 'a[i][j]' 
def transform(e, ignore_list=[], instances=None):
    global flag
    flag = False
    expr_elems = [get_expr(e) if instances is None else (instance[0] for instance in instances)]
    tree_root = e('/*')[0].getroottree()
    new_ignore_list = []
    for item in expr_elems:
        for expr_elem in item:
            expr_prev = expr_elem.getprevious()
            expr_prev = expr_prev if expr_prev is not None else expr_elem
            expr_prev_path = tree_root.getpath(expr_prev)
            if expr_prev_path in ignore_list: continue
            if len(expr_elem) < 5: continue
            # if the pointer is '*(a+i)'
            if len(expr_elem) <= 8 and expr_elem[0].text == '*' and expr_elem[1].text == '(' and expr_elem[
                3].text == '+' \
                    and expr_elem[5].text == ')':
                expr_elem[3].text = '['
                expr_elem[5].text = ']'
                del expr_elem[0]
                # After deleting a line, the subscript changes automatically, so the subscript of 'expr_elem' is 0
                del expr_elem[0]
                flag = True
            # if the pointer is '*(*(a+i)+j)'
            elif len(expr_elem) > 8:
                if expr_elem[0].text == '*' and expr_elem[2].text == '*' and expr_elem[
                    1].text == '(' \
                        and expr_elem[3].text == '(' and expr_elem[7].text == ')' and expr_elem[10].text == ')' \
                        and expr_elem[6].text == '+' and expr_elem[9].text == '+':
                    expr_elem[5].text = '['
                    expr_elem[7].text = ']'
                    expr_elem[8].text = '['
                    expr_elem[10].text = ']'
                    del expr_elem[0]
                    del expr_elem[0]
                    del expr_elem[0]
                    del expr_elem[0]
                    flag = True

            if flag:
                new_ignore_list.append(expr_prev_path)
    return flag, tree_root, new_ignore_list


def count_num(xml_path):
    count = 0
    e = init_parse(xml_path)
    expr_elems = get_expr(e)
    for expr_elem in expr_elems:
        if 6 <= len(expr_elem) <= 8:
            if expr_elem[0].text == '*' and expr_elem[1].text == '(' and expr_elem[
                3].text == '+' \
                    and expr_elem[5].text == ')':
                count = count + 1
        elif len(expr_elem) > 9:
            if expr_elem[0].text == '*' and expr_elem[2].text == '*' and expr_elem[1].text == '(' \
                    and expr_elem[3].text == '(' and expr_elem[7].text == ')' and expr_elem[10].text == ')' \
                    and expr_elem[6].text == '+' and expr_elem[9].text == '+':
                count = count + 1
    return count


# program's input port
def program_transform(xml_path):
    e = init_parse(xml_path)
    transform(e)
    save_tree_to_file(doc, './style/style.xml')


def program_transform_save_div(program_name, save_path):
    e = init_parse(os.path.join(save_path, program_name + '.xml'))
    transform(e)
    save_tree_to_file(doc, os.path.join(save_path, program_name + '.xml'))