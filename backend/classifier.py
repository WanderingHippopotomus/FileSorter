from .utils.config import SORT
import os
import re

img_re = '.*\.(jpg|jpeg|png|gif)'
vid_re = '.*\.(mp4|mp3|mov|m4a)'
docs_re = '.*\.(pdf|txt|docx|xlsx|xls|csv|ppt|pptx)'
misc_re = '.*\..*'

def classify_files() -> list | None:
    files = os.listdir()
    
    imgs = []
    vids = []
    docs = []
    misc = []
    
    images = None
    videos = None
    documents = None
    miscs = None
    
    for i in range(len(files)):
        if re.match(img_re, files[i]):
            imgs.append(files[i])
        elif re.match(vid_re, files[i]):
            vids.append(files[i])
        elif re.match(docs_re, files[i]):
            docs.append(files[i])
        else:
            if re.match(misc_re, files[i]):
                misc.append(files[i])
    
    if 'img' in SORT:
        images = imgs
    
    if 'vids' in SORT:
        videos = vids
    
    if 'docs' in SORT:
        documents = docs
    
    if 'misc' in SORT:
        miscs = misc
        
    return [images, videos, documents, miscs]