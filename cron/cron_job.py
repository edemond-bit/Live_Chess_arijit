from datetime import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
import shutil
from pathlib import Path
import re

def do(loc, file_name, file_src):
    # print(sid.__dict__)
    # for x in iter(sid.listFreqs()):
    #     print(x)
    # temp = re.compile("([a-zA-Z]+)([0-9]+)")
    # res = temp.match(file_src).groups()
    # name = file_src[:-5]
    # name = name + str(sid) + ".pgn"

    # split = re.split(r'\\|/', file_src)
    # orig_file_name = split[len(split) - 1]
    # if os.path.exists(file_src):

    shutil.copy(file_src, loc)
    # src = os.path.join(loc, orig_file_name)
    src = os.path.join(loc, file_src)
    des = os.path.join(loc, file_name + ".pgn")
    if os.path.exists(des):
        os.remove(des)
    os.rename(src, des)

def start(loc, file_name, file_src):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: do(loc, file_name, file_src), 'interval', seconds=20, id="file_upload")
    scheduler.start()