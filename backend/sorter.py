# Built by WanderingHippopotomus

import os, shutil
from .logger import logger
from .classifier import classify_files

def create_dir():
    try:
        os.mkdir('Images')
    except FileExistsError:
        logger.warning("Folder Images already exist.")
    try:
        os.mkdir('Videos')
    except FileExistsError:
        logger.warning("Folder Videos already exist.")

    os.makedirs('Documents\Word', exist_ok=True)
    os.makedirs('Documents\PPT', exist_ok=True)
    os.makedirs('Documents\PDF', exist_ok=True)
    os.makedirs('Documents\Excel', exist_ok=True)
    os.makedirs('Documents\Txt', exist_ok=True)
        
    try:
        os.mkdir('Miscs')
    except FileExistsError:
        logger.warning("Folder Miscs already exist.")

def _move_files(DIR,files,folder):
    moved = 0
    for item in files:
            try:
                shutil.move(f'{DIR}\{item}', f'{DIR}\Documents\{folder}')
                moved += 1
            except (PermissionError, FileNotFoundError):
                logger.error(f"{item} not found or moved, or not enough permission.")
    
    return moved
                
def sort_main(DIR:str) -> tuple:
    classified_files = classify_files()
    imgs = classified_files[0]
    vids = classified_files[1]
    docs = classified_files[2]
    word_doc = classified_files[3]
    txt_doc = classified_files[4]
    ppt_doc = classified_files[5]
    excel_doc = classified_files[6]
    pdf_doc = classified_files[7]
    miscs = classified_files[8]
    
    imgs_counter = 0
    if imgs:
        for img in imgs:
            try:
                shutil.move(f'{DIR}\{img}', f'{DIR}\Images')
                imgs_counter += 1
            except (PermissionError, FileNotFoundError):
                logger.error(f"{img} not found or moved, or not enough permission.")
                
    logger.info(f'Moved {imgs_counter} images.')
    
    vids_counter = 0
    if vids:
        for vid in vids:
            try:
                shutil.move(f'{DIR}\{vid}', f'{DIR}\Videos')
                vids_counter += 1
            except (PermissionError, FileNotFoundError):
                logger.error(f"{vid} not found or moved, or not enough permission.")
                
    logger.info(f'Moved {vids_counter} videos.')
    
    counter1 = counter2 = counter3 = counter4 = counter5 = 0 
    if docs:
        counter1 = _move_files(DIR,word_doc, 'Word')
        counter2 = _move_files(DIR,pdf_doc, 'PDF')
        counter3 = _move_files(DIR,excel_doc, 'Excel')
        counter4 = _move_files(DIR,ppt_doc, 'PPT')
        counter5 = _move_files(DIR,txt_doc, 'Txt')
    
    docs_counter = counter1 + counter2 + counter3 + counter4 + counter5
    
    logger.info(f'Moved {docs_counter} documents.')
        
    misc_counter = 0
    if miscs:
        for misc in miscs:
            try:
                shutil.move(f'{DIR}\{misc}', f'{DIR}\Miscs')
                misc_counter += 1
            except (PermissionError, FileNotFoundError):
                logger.error(f"{misc} not found or moved, or not enough permission.")

    logger.info(f'Moved {misc_counter} misc files.')
    
    total_files = len(imgs or []) + len(miscs or []) + len(vids or []) + len(docs or [])
    successfully_moved = imgs_counter + vids_counter + docs_counter + misc_counter
    error = total_files - successfully_moved
    
    return total_files, successfully_moved, error