# 功能说明
将照片及视频按拍摄日期（非文件的创建时间或者修改时间）进行目录分类，支持的文件格式有：JPG、HEIC、PDF、MP4、MOV
> 比如scanPath中IMG_1234.JPG是2022年06月08号拍摄，那么照片针对被移动到toPath/2022/06/目录中
## 典型场景
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
3. 修改config.ini里的配置，设置好scan_path和to_path
> scan_path：指定从哪个目录整理照片。
> to_path：指定照片整理到哪个目录。（比如Synology photos的场景就可以指定到用户目录下的Photos/PhotoLibrary/）
执行：
```py
python sync_photo_path.py
```
