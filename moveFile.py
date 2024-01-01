import os
import shutil

dirPath = '/mnt/d/BaiduNetdiskDownload/课程'
outPath = '/mnt/d/BaiduNetdiskDownload/课程-字幕'
ext = '.vtt'

for root, dirs, files in os.walk(dirPath):
    for file in files:
        if not file.endswith(ext):
            continue

        originPath = os.path.join(root, file)
        targetPath = originPath.replace(dirPath, outPath)
        if not os.path.exists(os.path.dirname(targetPath)):
            os.makedirs(os.path.dirname(targetPath))

        print(f'{originPath} -> {targetPath}')
        shutil.copyfile(originPath, targetPath)
