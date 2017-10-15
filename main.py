#-*- coding: utf-8 -*-

import argparse
from lib import *

def get_notebook(args):
    if args.box != None:
        notebook =get_notebook_by_guid(args.box)
        if notebook != None:
            return notebook.guid
    elif args.name!=None:
        return get_notebook_by_name(args.name)
    return None

def list_func(args):
    notebook_guid = get_notebook(args)
    if notebook_guid != None:
        print_notes_in_notebooks(notebook_guid)
    else:
        print_all_notebooks()

def init_func(args):
    print args
    create_notebook(args.name)

def push_func(args):
    notebook_guid = get_notebook(args)
    if notebook_guid == None:
        print '未找到指定仓库'
        return
    else:
        for file in args.files:
            if not os.path.exists(file):
                print '文件 %s 不存在' % file
            else:
                push('\\'+os.path.basename(file), file, notebook_guid)

def pushdir_func(args):
    notebook_guid = get_notebook(args)
    if notebook_guid == None:
        print '未找到指定仓库'
        return
    else:
        if not os.path.exists(args.dir):
            print '目录 %s 不存在' % file
        else:
            push_dir(notebook_guid, args.dir)

def pull_func(args):
    notebook_guid = get_notebook(args)
    if notebook_guid == None:
        print '未找到指定仓库'
        return
    else:
        if args.text != None:
            for text in args.text:
                note = get_note(text)
                if note != None:
                    pull(note, args.dir)
                else:
                    print '文本 %s 未找到' % text
        else:
            for textname in args.textname:
                note = in_notebooks(textname, notebook_guid)
                if note != None:
                    pull(note, args.dir)
                else:
                    print '文本 %s 未找到' % textname

def pullbox_func(args):
    notebook_guid = get_notebook(args)
    if notebook_guid == None:
        print '未找到指定仓库'
        return
    else:
        pull_from_notebooks(notebook_guid, args.dir)

def remove_func(args):
    try:
        remove_note(args.text)
    except:
        print '删除失败'

def drop_func(args):
    notebook_guid = get_notebook(args)
    if notebook_guid == None:
        print '未找到指定仓库'
        return
    try:
        remove_notebook(notebook_guid)
    except Exception as e:
        print '删除失败'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='操作命令')

    init_cmd = subparsers.add_parser('init', help='新建一个仓库', description='新建一个仓库')
    init_cmd.add_argument('name', help='仓库名称')
    init_cmd.set_defaults(func=init_func)

    push_cmd = subparsers.add_parser('push', help='添加一个或多个文本到仓库', description='添加一个或多个文本到仓库')
    group = push_cmd.add_mutually_exclusive_group()
    group.add_argument('-b', '--box', help='仓库id')
    group.add_argument('-n', '--name', help='仓库名称')
    push_cmd.add_argument('files', help='文本路径', nargs='*')
    push_cmd.set_defaults(func=push_func)

    pushdir_cmd = subparsers.add_parser('pushdir', help='添加目录下的所有文本到仓库', description='添加目录下的所有文本到仓库')
    group = pushdir_cmd.add_mutually_exclusive_group()
    group.add_argument('-b', '--box', help='仓库id')
    group.add_argument('-n', '--name', help='仓库名称')
    pushdir_cmd.add_argument('dir', help='目录')
    pushdir_cmd.set_defaults(func=pushdir_func)

    pull_cmd = subparsers.add_parser('pull', help='从仓库拉取指定文本到本地', description='从仓库拉取指定文本到本地')
    group = pull_cmd.add_mutually_exclusive_group()
    group.add_argument('-b', '--box', help='仓库id')
    group.add_argument('-n', '--name', help='仓库名称')
    group = pull_cmd.add_mutually_exclusive_group()
    group.add_argument('-t', '--text', help='文本guid', nargs='*')
    group.add_argument('-tn', '--textname', help='文本名称', nargs='*')
    pull_cmd.add_argument('dir', help='拉取目录')
    pull_cmd.set_defaults(func=pull_func)

    pullbox_cmd = subparsers.add_parser('pullbox', help='拉取仓库中的所有文本到本地', description='拉取仓库中的所有文本到本地')
    group = pullbox_cmd.add_mutually_exclusive_group()
    group.add_argument('-b', '--box', help='仓库id')
    group.add_argument('-n', '--name', help='仓库名称')
    pullbox_cmd.add_argument('dir', help='拉取目录')
    pullbox_cmd.set_defaults(func=pullbox_func)

    list_cmd = subparsers.add_parser('list', help='列出所有仓库的信息/列出指定仓库中的所有文本', description='列出所有仓库/指定仓库中的所有文本')
    group = list_cmd.add_mutually_exclusive_group()
    group.add_argument('-b', '--box', help='仓库id')
    group.add_argument('-n', '--name', help='仓库名称')
    list_cmd.set_defaults(func=list_func)

    remove_cmd = subparsers.add_parser('remove', help='删除指定id的文本', description='删除指定id的文本')
    remove_cmd.add_argument('text', help='文本id')
    remove_cmd.set_defaults(func=remove_func)

    drop_cmd = subparsers.add_parser('drop', help='删除指定仓库', description='删除指定仓库')
    group = drop_cmd.add_mutually_exclusive_group()
    group.add_argument('-b', '--box', help='仓库id')
    group.add_argument('-n', '--name', help='仓库名称')
    drop_cmd.set_defaults(func=drop_func)

    args = parser.parse_args()
    args.func(args)