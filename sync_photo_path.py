import os,sys,shutil,grp, pwd, configparser, time
import exifread
import xml.dom.minidom
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

configParser = configparser.ConfigParser()
configParser.read('./config.ini', encoding='utf-8')

if not configParser.has_section('path'):
    print('请在config.ini中配置[path]并配置scan_path和to_path信息')
    sys.exit()

itemsDict = dict(configParser.items('path'))

if not itemsDict or 'scan_path' not in itemsDict or 'to_path' not in itemsDict:
    print('请在config.ini中配置scan_path和to_path，指定扫描路径和目的地路径')
    sys.exit()

scanPath = itemsDict['scan_path'].strip('"').strip()
toPath = itemsDict['to_path'].strip('"').strip()

logPath = "./log"
if not os.path.exists(logPath):
    os.makedirs(logPath)
logFile = os.path.join(logPath, time.strftime("%Y%m%d%H%M%S", time.localtime())+".log")
fo = open(logFile, 'a')

def log(*msg):
    global fo
    logMsg = ' '.join(msg)
    fo.write(logMsg+"\n")
    print(logMsg)

def syncFilePath(file):
    global toPath

    if not os.path.exists(file):
        log(file, "文件不存在")
        return 0

    filePath, fileName = os.path.split(file)

    #获取新文件的地址及文件名
    fileSuffix = os.path.splitext(fileName)[-1][1:].lower()
    if fileSuffix in ['jpeg', 'jpg', 'heic']:
        f = open(file, "rb")
        tags = exifread.process_file(f)
        exifDateKey = 'EXIF DateTimeOriginal'
        imageDateKey = 'Image DateTime'
        #过滤没有拍摄时间的照片
        if exifDateKey not in tags:
            if imageDateKey not in tags:
                log(file, "图片没有拍摄时间，过滤不处理")
                return 0
            else:
                dateTimeOriginal = tags[imageDateKey].values
        else:
            dateTimeOriginal = tags[exifDateKey].values

        toNewFile = os.path.join(toPath, dateTimeOriginal[0:4], dateTimeOriginal[5:7], fileName)
    elif fileSuffix in ['mp4', 'mov', 'm4v']:
        #取媒体拍摄时间
        metadata = extractMetadata(createParser(file))
        if (not metadata):
            log(file, "解析失败，无法处理")
            return 0
        metaCreateDate = metadata.get('creation_date')
        toNewFile = os.path.join(toPath, str(metaCreateDate.year), str(metaCreateDate.month).zfill(2), fileName)
    elif fileSuffix in ['png']:
        im = Image.open(file)
        if "XML:com.adobe.xmp" in im.info:
            xmlDom = xml.dom.minidom.parseString(im.info.get("XML:com.adobe.xmp"))
            root = xmlDom.documentElement
            dateCreatedElement = root.getElementsByTagName('photoshop:DateCreated')
            pngCreateDate = dateCreatedElement[0].firstChild.data
            toNewFile = os.path.join(toPath, pngCreateDate[0:4], pngCreateDate[5:7], fileName)
        else:
            #当PNG没有xmp信息时，取文件的修改时间
            log(file, "没有xmp信息，用了系统修改时间")
            timeInfo = time.localtime(os.stat(file).st_mtime)
            toNewFile = os.path.join(toPath, time.strftime('%Y', timeInfo), time.strftime('%m', timeInfo), fileName)
    else:
        log(file, "该文件类型不能处理，跳过")
        return 0

    #如果变更后的文件地址跟现在一样，那就不处理
    if file == toNewFile:
        return 0

    if os.path.exists(toNewFile):
        log(toNewFile, "跟目的地文件夹中现有文件同名了，过滤不处理")
        return 0

    toNewFilePath = os.path.split(toNewFile)[0]
    if not os.path.exists(toNewFilePath):
        #如果目的地目录不存在，则创建目录，user和group信息用源照片的user和group信息
        userName = os.popen("ls -al '"+file+"' |awk '{print $3}'").read().strip()
        groupName = os.popen("ls -al '"+file+"' |awk '{print $4}'").read().strip()
        uid = pwd.getpwnam(userName).pw_uid
        gid = grp.getgrnam(groupName).gr_gid
        os.makedirs(toNewFilePath)
        os.chown(toNewFilePath, uid, gid)

    shutil.move(file, toNewFile)
    log(file, toNewFile)
    #如果源目录是群晖的相册目录，删除用于全局搜索的系统文件
    eaDir = os.path.join(filePath, "@eaDir", fileName)
    if os.path.exists(eaDir):
        shutil.rmtree(eaDir)
    return 1

def scan():
    global scanPath

    g = os.walk(scanPath)
    for path,dirList,fileList in g:
        
        for fileName in fileList:
            #过滤群晖用于全局搜索的系统文件
            if "@eaDir" in fileName or "@eaDir" in path:
                continue

            file = os.path.join(path, fileName)
            result = syncFilePath(file)

#同步指定目录的照片及视频
scan()

#用于单个文件测试
#syncFilePath("/path/test/IMG_4135.m4v")

fo.close()
