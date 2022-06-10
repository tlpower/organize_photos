import os
import exifread
import imghdr
import shutil

scanPath = "/var/services/homes/tlpower/Photos/PhotoLibrary/2018/11"
toPath = "/var/services/homes/tlpower/Photos/PhotoLibrary/"

def fixFilePath(file):
    global toPath

    fileName = file.split("/")[-1]

    #过滤非图片文件
    fileSuffix = os.path.splitext(fileName)[-1][1:].lower()
    if fileSuffix not in ('jpeg', 'jpg', 'heic'):
        return "filter"

    f = open(file, "rb")
    tags = exifread.process_file(f)
    dateKey = 'EXIF DateTimeOriginal'

    #过滤没有拍摄时间的照片
    if dateKey not in tags:
        return "filter"

    dateTimeOriginal = tags[dateKey].values

    toNewFile = os.path.join(toPath, dateTimeOriginal[0:4], dateTimeOriginal[5:7], fileName)

    #如果变更后的文件地址跟现在一样，那就不处理
    if file == toNewFile:
        return "filter"

    shutil.move(file, toNewFile)
    print(file, toNewFile)
    return "success"

#单张照片迁移测试
#fixFilePath("/var/services/homes/tlpower/Photos/PhotoLibrary/2018/11/IMG_1988.JPG")

g = os.walk(scanPath)
for path,dirList,fileList in g:
    
    for fileName in fileList:
        #过滤群晖用于全局搜索的系统文件
        if "@eaDir" in fileName or "@eaDir" in path:
            continue

        file = os.path.join(path, fileName)
        result = fixFilePath(file)
        if ("filter" == result):
            continue
