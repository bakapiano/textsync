# 简介
利用evernote接口实现的文本同步脚本
```
usage: main.py [-h] {init,push,pushdir,pull,pullbox,list,remove,drop} ...

optional arguments:
  -h, --help            show this help message and exit

操作命令:
  {init,push,pushdir,pull,pullbox,list,remove,drop}
    init                新建一个仓库
    push                添加一个或多个文本到仓库
    pushdir             添加目录下的所有文本到仓库
    pull                从仓库拉取指定文本到本地
    pullbox             拉取仓库中的所有文本到本地
    list                列出所有仓库/指定仓库中的所有文本
    remove              删除指定id的文本
    drop                删除指定仓库
```
# 准备工作
1.安装evernote sdk for python
```
pip install evernote
```
2.从[Evernote开发者](https://sandbox.evernote.com/ "Evernote开发者")获取一个开发Token
# 命令详细
##init
```
usage: main.py init [-h] name

新建一个仓库

positional arguments:
  name        仓库名称

optional arguments:
  -h, --help  show this help message and exit
```
##push
```
 usage: main.py push [-h] [-b BOX | -n NAME] [files [files ...]]

添加一个或多个文本到仓库

positional arguments:
  files                 文本路径

optional arguments:
  -h, --help            show this help message and exit
  -b BOX, --box BOX     仓库id
  -n NAME, --name NAME  仓库名称
  ```
##pushdir
```
usage: main.py pushdir [-h] [-b BOX | -n NAME] dir

添加目录下的所有文本到仓库

positional arguments:
  dir                   目录

optional arguments:
  -h, --help            show this help message and exit
  -b BOX, --box BOX     仓库id
  -n NAME, --name NAME  仓库名称
```
##pull
```
usage: main.py pull [-h] [-b BOX | -n NAME] [-t [TEXT [TEXT ...]] | -tn
                    [TEXTNAME [TEXTNAME ...]]]
                    dir

从仓库拉取一个或多个文本到本地

positional arguments:
  dir                   拉取目录

optional arguments:
  -h, --help            show this help message and exit
  -b BOX, --box BOX     仓库id
  -n NAME, --name NAME  仓库名称
  -t [TEXT [TEXT ...]], --text [TEXT [TEXT ...]]
                        文本guid
  -tn [TEXTNAME [TEXTNAME ...]], --textname [TEXTNAME [TEXTNAME ...]]
                        文本名称
```
##pullbox
```
拉取仓库中的所有文本到本地

positional arguments:
  dir                   拉取目录

optional arguments:
  -h, --help            show this help message and exit
  -b BOX, --box BOX     仓库id
  -n NAME, --name NAME  仓库名称
```
##list
```
usage: main.py list [-h] [-b BOX | -n NAME]

列出所有仓库/指定仓库中的所有文本

optional arguments:
  -h, --help            show this help message and exit
  -b BOX, --box BOX     仓库id
  -n NAME, --name NAME  仓库名称
```
##drop
```
usage: main.py drop [-h] [-b BOX | -n NAME]

删除指定仓库

optional arguments:
  -h, --help            show this help message and exit
  -b BOX, --box BOX     仓库id
  -n NAME, --name NAME  仓库名称
```
##remove
```
usage: main.py remove [-h] text

删除指定id的文本

positional arguments:
  text        文本id

optional arguments:
  -h, --help  show this help message and exit
```
##TODO
滋磁Linux环境下使用
