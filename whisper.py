import asyncio
import os

dirPath = '/mnt/d/BaiduNetdiskDownload/课程'
cliPath = '/home/win/miniconda3/envs/whisper/bin/whisper-ctranslate2'
computeArgs = ['--compute_type', 'int8']
cliArgs = ['--model', 'small', '--vad_filter', 'True', '--language', 'zh', '-f', 'vtt',
           '--initial_prompt', '请使用简体中文', '--local_files_only', 'True']
fileList = [os.path.join(root, file) for root, dirs, files in os.walk(dirPath) for file in files]
fileList = [i for i in filter(lambda e: e.endswith('.mp4'), fileList)]
batchSize = 1
currentIdx = 0


async def exec(fileName, semaphore: asyncio.Semaphore):
    async with semaphore:
        global currentIdx
        currentIdx = 1 + currentIdx
        print(f'[{currentIdx}/{len(fileList)}] starting... {fileName}')

        try:
            vttPath = os.path.splitext(fileName)[0] + '.vtt'
            if os.path.exists(vttPath):
                print(f'skipping {fileName}')
                return
            proc = await asyncio.create_subprocess_exec(cliPath, fileName, '-o', os.path.dirname(fileName), *cliArgs)
            await proc.wait()
            if proc.returncode != 0:
                print(f'error {fileName}')
        except Exception as e:
            print(currentIdx, fileName, e)


async def main():
    semaphore = asyncio.Semaphore(batchSize)
    await asyncio.gather(*[exec(i, semaphore) for i in fileList])


asyncio.run(main())
