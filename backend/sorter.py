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
    try:
        os.mkdir('Documents')
    except FileExistsError:
        logger.warning("Folder Documents already exist.")
    try:
        os.mkdir('Miscs')
    except FileExistsError:
        logger.warning("Folder Miscs already exist.")

def sort_main(DIR):
    classified_files = classify_files()
    imgs = classified_files[0]
    vids = classified_files[1]
    docs = classified_files[2]
    miscs = classified_files[3]
    
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
        
    docs_counter = 0
    if docs:
        for doc in docs:
            try:
                shutil.move(f'{DIR}\{doc}', f'{DIR}\Documents')
                docs_counter += 1
            except (PermissionError, FileNotFoundError):
                logger.error(f"{doc} not found or moved, or not enough permission.")
                
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