在搭群晖之前，我们通常会手动备份手机里的照片。
有了群晖以后，我们除了用Synology photos备份手机里的照片以外，还希望把以前手动保存的照片放到Synology photos相册里来。
这个Python程序主要是用于将手动保存的照片按Synology photos的目录格式迁移过来。

# 前期准备
执行前，需要先执行安装一个Python Module
```linux
pip install exifread,hachoir,pillow
```
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
