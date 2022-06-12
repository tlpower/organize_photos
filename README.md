在搭群晖之前，我们通常会手动备份手机里的照片。
有了群晖以后，我们除了用Synology photos备份手机里的照片以外，还希望把以前手动保存的照片放到Synology photos相册里来。
这个Python程序主要是用于将手动保存的照片按Synology photos的目录格式迁移过来。

# 前期准备
执行前，需要先执行安装一个Python Module
```linux
pip install exifread,hachoir,pyexiv2
```

## 可能发生的问题
使用pyexiv2的module时，可能会遇到以下问题：
- 在 Linux 上使用 pyexiv2 时，你可能遇到以下异常：
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.so'))
      self._handle = _dlopen(self._name, mode)
  OSError: /lib64/libm.so.6: version `GLIBC_2.29' not found (required by /usr/local/lib/python3.6/site-packages/pyexiv2/lib/libexiv2.so)
  ```
  - 这是因为 pyexiv2 在编译时使用了 GLIBC 2.29 ，它在 2019 年 1 月发布。你需要升级你的 GLIBC 库，或者升级 Linux 发行版。
  - 你可以执行 `ldd --version` 或者 `ls -l /lib/libc.so.*` 或者 `/lib/libc.so.6` 查看 GLIBC 库的版本。

- 在 MacOS 上使用 pyexiv2 时，你可能遇到以下异常：
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.dylib'))
      self._handle = _dlopen(self._name, mode)
  OSError: dlopen(/Library/Python/3.8/site-packages/pyexiv2/lib/libexiv2.dylib, 6): Library not loaded: /usr/local/lib/libintl.8.dylib
  Referenced from: /Library/Python/3.8/site-packages/pyexiv2/lib/libexiv2.dylib
  Reason: image not found
  ```
  - 这是因为 libintl.8.dylib 不存在。你需要执行 `brew install gettext` 。

- 在 Windows 上使用 pyexiv2 时，你可能遇到以下异常：
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'exiv2.dll'))
      self._handle = _dlopen(self._name, mode)
  FileNotFoundError: Could not find module '...\lib\site-packages\pyexiv2\lib\exiv2.dll' (or one of its dependencies). Try using the full path with constructor syntax.
  ```
  - 这是因为该路径的 exiv2.dll 文件不存在，或者你需要安装 [Microsoft Visual C++ 2015-2019](https://visualstudio.microsoft.com/downloads/#microsoft-visual-c-redistributable-for-visual-studio-2019)

其它详情参考这里： [pyexiv2-Tutorial-cn.md](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md)

# 执行
1. 使用终端工具SSH进入群晖
> 进入群晖DSM，打开控制面板->终端机和SNMP->终端机->勾选“启动SSH功能”
2. SSH连接并切换至root用户
```shell
sudo -i
```
3. 修改python文件里的配置，设置好scanPath和toPath
> scanPath：表示你需要从哪个目录迁移照片到Synology photos  
> toPath：表示Synology photos照片库地址
执行：
```py
python sync_photo_path.py
```
