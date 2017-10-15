#-*- coding: utf-8 -*-

import sys, os, re
import hashlib
from datetime import datetime, date

try:
    from evernote.api.client import EvernoteClient
    import evernote.edam.type.ttypes as Types
    import evernote.edam.notestore.ttypes as NoteTypes
except:
    print ('evernote扩展初始化失败...')
    sys.exit(-1)

file_list     = []
file_realpath = {}
running_path  = os.getcwd()
dev_token     = ""

get_client     = lambda : EvernoteClient(token=dev_token)
get_note_store = lambda : get_client().get_note_store()
get_note_books = lambda : get_note_store().listNotebooks()

def calc_MD5(conternt):
    md5 = hashlib.md5()
    md5.update(conternt)
    return md5.hexdigest()

def file_to_note(title, content, md5, notebook_id):
    note              = Types.Note()
    note.notebookGuid = notebook_id
    note.title        = title
    note.content      = '''<?xml version="1.0" encoding="UTF-8"?>
                           <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
                           <en-note>
                           (CONTENT_START)%s(CONTENT_END)
                           (MD5_START)%s(MD5_END)
                           </en-note>''' % (content, md5)
    return note

def create_notebook(name):
    notebook      = Types.Notebook()
    notebook.name = name
    return get_note_store().createNotebook(dev_token, notebook)

def get_notebook_by_guid(notebook_guid):
    lists = get_note_books()
    for notebook in lists:
        if notebook.guid.startswith(notebook_guid):
            return notebook
    return None

def get_notebook_by_name(notebook_name):
    lists = get_note_books()
    for notebook in lists:
        if notebook.name == notebook_name:
            return notebook
    return None

def create_note(note):
    note = get_note_store().createNote(dev_token, note)
    return note

def print_all_notebooks():
    note_books = get_note_books()
    print ('| 仓库id                           | 仓库名称 | 创建时间')
    for box in note_books:
        print box.guid, box.name, box.serviceCreated

def list_notes_in_notebooks(notebook_id):
    filter              = NoteTypes.NoteFilter()
    filter.notebookGuid = notebook_id
    notes               = get_note_store().findNotes(dev_token, filter, 0, 100).notes
    return notes

def print_notes_in_notebooks(notebook_id):
    notes = list_notes_in_notebooks(notebook_id)
    print ('| 文本id                           | 文本名称 | 创建时间')
    for f in notes:
        print "%s %s %s" % (f.guid, f.title, f.created)

def init(target_path):
    global file_list, file_realpath, hash
    file_list     = []
    file_realpath = {}
    queue         = ["\\"]

    while len(queue) > 0:
        now_dir = os.listdir(target_path+queue[0])
        for d in now_dir:
            if os.path.isdir(target_path+queue[0]+d):
                queue.append(queue[0]+d+'\\')
            else:
                file_name                = queue[0]+d
                file_realpath[file_name] = target_path+file_name
                file_list.append(file_name)
        queue.pop(0)

def in_notebooks(title, notebook_id):
    filter              = NoteTypes.NoteFilter()
    filter.notebookGuid = notebook_id
    filter.name         = "intitle:%s" % title
    results = get_note_store().findNotes(dev_token, filter, 0, 100).notes
    for note in results:
        if note.title == title:
            return note.guid
    return None

def get_note(note_guid):
    try:
        return get_note_store().getNote(dev_token, note_guid, True, True, False, False)
    except:
        return None

def remove_note(guid):
    get_note_store().deleteNote(dev_token, guid)

def remove_notebook(guid):
    get_note_store().expungeNotebook(dev_token, guid)

def update_note(pre_note_guid, note, content, md5):
    note.content = content
    newnote = file_to_note(note.title, content, md5, note.notebookGuid)
    remove_note(pre_note_guid)
    create_note(newnote)

def file_already_exist(file_name):
    print"文件: %s 已经存在，是否覆盖？[Y/N]" % file_name
    flag = raw_input()
    if flag.startswith("Y"):
        return True
    else:
        return False

def split_note_content(content):
    text            = {}
    content         = content.split('<en-note>')[-1].split('</en-note>')[0]
    text["content"] = content.split('(CONTENT_START)')[-1].split('(CONTENT_END)')[0]
    text["md5"]     = content.split('(MD5_START)')[-1].split('(MD5_END)')[0]
    return text

def push(file_name, file_path, notebook_id):
    with open(file_path, 'r') as f:
        content = f.read()

    note_guid = in_notebooks(file_name, notebook_id)
    if note_guid != None:
        note = get_note(note_guid)
        text = split_note_content(note.content)
        md5  = calc_MD5(content)
        if  md5 != text["md5"] and file_already_exist(file_name):
            update_note(note_guid, note, content, md5)

    else:
        note = file_to_note(file_name, content, calc_MD5(content), notebook_id)
        create_note(note)

def push_dir(notebook_id, dir=None):
    if dir == None:
        init(running_path)
        path = running_path
    else:
        init(dir)

    update_count = 0
    for file in file_list:
        file_name = file
        try:
            print "正在上传 %s ..." % file
            file_name = file
            push(file_name, file_realpath[file], notebook_id)
        except Exception as e:
            print "文件 %s 上传失败..." % file
            print e
        else:
            update_count += 1
            print "文件 %s 上传成功..." % file

    print "目录 %s 上传完成, 成功上传 %d 个文件..." % (dir, update_count)

def pull(note, target_path=None):
    if not note == None:
        if not target_path.endswith('\\'):
            target_path = target_path + '\\'
        note = get_note(note)
        text = split_note_content(note.content)
        content = text['content']
        file_path = target_path + note.title.split('\\')[-1]
        dir = os.path.split(file_path)[0]
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
            if os.path.exists(file_path) == False or file_already_exist(file_path):
                with open(file_path, 'w+') as f:
                    f.write(content)
        except:
            pass
    else:
        print "未找到指定文本"

def pull_from_notebooks(notebook_id, target_path):
    if target_path == None:
        target_path = running_path
    if target_path.endswith('\\'):
        target_path = target_path[:-1]

    note_list      = list_notes_in_notebooks(notebook_id)
    download_count = 0
    for note in note_list:
        note      = get_note(note.guid)
        text      = split_note_content(note.content)
        content   = text['content']
        file_path = target_path + note.title
        dir       = os.path.split(file_path)[0]

        print "正在同步 %s ..." % note.title
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
            if os.path.exists(file_path) == False or file_already_exist(file_path):
                with open(file_path, 'w+') as f:
                    f.write(content)
        except:
            print "文件 %s 同步失败 ..." % note.title
        else:
            download_count += 1
            print "文件 %s 同步成功..." % note.title

    print "仓库 %s 同步完成，成功同步 %d 个文件..." % (notebook_id, download_count)