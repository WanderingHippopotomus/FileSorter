from .utils.config import SORT
import os
import re

img_re = re.compile('.*\.(jpg|jpeg|png|gif|bmp|webp|tiff|tif|svg|heic|ico)$', re.IGNORECASE)
vid_re = re.compile('.*\.(mp4|mov|avi|mkv|wmv|flv|webm|mpeg|mpg|3gp|m4v)$', re.IGNORECASE)
audio_re = re.compile('.*\.(mp3|wav|flac|aac|ogg|m4a|wma)$', re.IGNORECASE)
docs_re = re.compile('.*\.(pdf|txt|doc|docx|rtf|odt|xls|xlsx|csv|ppt|pptx|odp)$', re.IGNORECASE)
code_re = re.compile('.*\.(py|js|ts|java|cpp|c|cs|go|rs|php|html|css|json|xml|yaml|yml|sql|ipynb)$', re.IGNORECASE)
archive_re = re.compile('.*\.(zip|rar|7z|tar|gz|bz2|xz|iso)$', re.IGNORECASE)
exe_re = re.compile('.*\.(exe|msi|bat|cmd|ps1|apk|deb|rpm|appimage)$', re.IGNORECASE)
word_re = re.compile('.*\.(docx|doc)$', re.IGNORECASE)
txt_re = re.compile('.*\.txt$', re.IGNORECASE)
pdf_re = re.compile('.*\.(pdf)$', re.IGNORECASE)
excel_re = re.compile('.*\.(xlsx|xls|csv)$', re.IGNORECASE)
ppt_re = re.compile('.*\.(ppt|pptx)$', re.IGNORECASE)
misc_re = re.compile('.*\..*$', re.IGNORECASE)

def classify_files() -> list:
    files = os.listdir()
    
    imgs = []
    vids = []
    auds = []
    codes = []
    archs = []
    exes = []
    docs = []
    word = []
    excel = []
    pdf = []
    ppt = []
    txt = []
    misc = []
    other_docs = []
    
    images = []
    audios = []
    pro_codes = []
    archives = []
    executables = []
    videos = []
    documents = []
    miscs = []
    
    for file in files:
        if img_re.match(file):
            imgs.append(file)
        elif vid_re.match(file):
            vids.append(file)
        elif docs_re.match(file):
            docs.append(file)
        elif audio_re.match(file):
            auds.append(file)
        elif code_re.match(file):
            codes.append(file)
        elif archive_re.match(file):
            archs.append(file)
        elif exe_re.match(file):
            exes.append(file)
        else:
            if misc_re.match(file):
                misc.append(file)
    
    for doc in docs:
        if word_re.match(doc):
            word.append(doc)
        elif excel_re.match(doc):
            excel.append(doc)
        elif pdf_re.match(doc):
            pdf.append(doc)
        elif ppt_re.match(doc):
            ppt.append(doc)
        elif txt_re.match(doc):
            txt.append(doc)
        else:
            other_docs.append(doc)
            
    if 'img' in SORT:
        images = imgs
    
    if 'vids' in SORT:
        videos = vids
    
    documents = []
    word_doc = []
    txt_doc = []
    ppt_doc = []
    excel_doc = []
    pdf_doc = []
    other_doc = []
    if 'docs' in SORT:
        documents = docs
        word_doc = word
        txt_doc = txt
        ppt_doc = ppt
        excel_doc = excel
        pdf_doc = pdf
        other_doc = other_docs
        
    if 'misc' in SORT:
        miscs = misc
    
    if 'audio' in SORT:
        audios = auds
    
    if 'code' in SORT:
        pro_codes = codes
    
    if 'exe' in SORT:
        executables = exes
    
    if 'arch' in SORT:
        archives = archs
    
    return [images, 
            videos, 
            documents, 
            word_doc, 
            txt_doc, 
            ppt_doc, 
            excel_doc, 
            pdf_doc, 
            miscs, 
            other_doc, 
            archives, 
            executables, 
            pro_codes, 
            audios]