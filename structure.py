#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import asyncio

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--depth',type=int,default=5,help="递归深度")
    parser.add_argument('-p','--path',type=str,default=os.getcwd(),help="路径")
    parser.add_argument('-o','--output',type=str,default='./output.txt',help="输出文件")
    parser.add_argument('-s','--skip',type=bool,default=True)
    args = parser.parse_args()
    return args.depth, args.path, args.output, args.skip

async def draw(f:str, current:int, depth:int, path:str, skipDotfiles:bool=True):
    entries = os.listdir(path)
    if len(entries) == 0:
         f.write('{}├─ <Empty>\n'.format("|    "*current))
    elif current == depth:
         f.write('{}|  ...\n'.format("|    "*current))
         return
    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            f.write("{}├─ {}\n".format("|    "*current,entry))
    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            f.write("{}├─ /{}:\n".format("|    "*current,entry))
            if not (entry.startswith(".")):
                await draw(f,current+1,depth,full_path,skipDotfiles)

async def main():
    depth, path, output, skip = parseArgs()
    f = open(output, 'w+')
    await draw(f,0,depth,path,skip)
    print("任务完成")
    

if __name__ == '__main__':
	asyncio.run(main())

