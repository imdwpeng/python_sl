# python爬虫

 - python@3.9.1
 - pyqt5@5.12.2
 - pyinstaller@4.1

## 静态资源打包进exe

- 在 `resource.qrc` 中新增需要的静态资源

- 执行指令将 `qrc` 转换成 `py` 文件

```
pyrcc5 -o resource.py resource.qrc
```

- 在对应 `py` 文件中引入

```
import resource

QIcon(':/close.ico')  # 注意 `:` 必须
```

## 打包构建

```
pyinstaller -F -w --name=小牛爬虫 --icon=ox.ico index.py
```


