<!--
 * @Author: Dong
 * @Date: 2021-01-06 09:03:36
 * @LastEditors: Dong
 * @LastEditTime: 2021-01-06 12:51:19
-->
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

先执行上一步，将静态资源转换成 `py` 格式
然后进行打包

### window系统

用 `pyinstaller` 打包
```
pyinstaller -F -w --name=小牛爬虫 --icon=ox.ico index.py
```

### mac系统

用 `py2app` 打包（因为用 `pyinstaller` 打包时，图片资源不显示）
```
py2applet --make-setup index.py ox.icns
python3 setup.py py2app
```


