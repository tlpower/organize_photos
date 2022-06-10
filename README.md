在搭群晖之前，我们通常会手动备份手机里的照片。
有了群晖以后，我们除了用Synology photos备份手机里的照片以外，还希望把以前手动保存的照片放到Synology photos相册里来。
这个Python文件主要是用于将自动保存的照片按Synology photos的目录格式迁移过来。

执行前，需要先执行安装一个Python Module
```linux
pip install exifread
```

然后需要改一下文件里的配置，设置好scanPath和toPath
scanPath：表示你需要从哪个目录迁移照片到Synology photos
toPath：表示Synology photos照片库地址
