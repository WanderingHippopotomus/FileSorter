from .utils.config import SORT
import os
import re

img_re = '.*\.(jpg|jpeg|png|gif)'
vid_re = '.*\.(mp4|mp3|mov|m4a)'
docs_re = '.*\.(pdf|txt|docx|xlsx|xls|csv|ppt|pptx|doc)'
word_re = '.*\.(docx|doc)'
txt_re = '.*\.txt'
pdf_re = '.*\.(pdf)'
excel_re = '.*\.(xlsx|xls|csv)'
ppt_re = '.*\.(ppt|pptx)'
misc_re = '.*\..*'

def classify_files() -> list | None:
    files = os.listdir()
    
    imgs = []
    vids = []
    docs = []
    word = []
    excel = []
    pdf = []
    ppt = []
    txt = []
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
    
    for i in range(len(docs)):
        if re.match(word_re, docs[i]):
            word.append(docs[i])
        elif re.match(excel_re, docs[i]):
            excel.append(docs[i])
        elif re.match(pdf_re, docs[i]):
            pdf.append(docs[i])
        elif re.match(ppt_re, docs[i]):
            ppt.append(docs[i])
        elif re.match(txt_re, docs[i]):
            txt.append(docs[i])
            
    if 'img' in SORT:
        images = imgs
    
    if 'vids' in SORT:
        videos = vids
    
    if 'docs' in SORT:
        documents = docs
        word_doc = word
        txt_doc = txt
        ppt_doc = ppt
        excel_doc = excel
        pdf_doc = pdf
        
    if 'misc' in SORT:
        miscs = misc
        
    return [images, videos, documents, word_doc, txt_doc, ppt_doc, excel_doc, pdf_doc, miscs]