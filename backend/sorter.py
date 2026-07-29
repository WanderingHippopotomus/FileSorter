# Built by WanderingHippopotomus

import os, shutil
from .logger import logger
from .classifier import classify_files
from pathlib import Path
from typing import Any
def _unique_path(dest: str) -> str:
    path = Path(dest)
    
    if not path.exists():
        return str(path)
    
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    
    counter = 1
    
    while True:
        new_path = parent / f'{stem} ({counter}){suffix}'
        
        if not new_path.exists():
            return str(new_path)
        
        counter += 1 

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
        os.mkdir('Audios')
    except FileExistsError:
        logger.warning("Folder Videos already exist.")
    try:
        os.mkdir('Archives')
    except FileExistsError:
        logger.warning("Folder Videos already exist.")
    try:
        os.mkdir('Executables')
    except FileExistsError:
        logger.warning("Folder Videos already exist.")
    try:
        os.mkdir('Codes')
    except FileExistsError:
        logger.warning("Folder Videos already exist.")

    os.makedirs(r'Documents\Word', exist_ok=True)
    os.makedirs(r'Documents\PPT', exist_ok=True)
    os.makedirs(r'Documents\PDF', exist_ok=True)
    os.makedirs(r'Documents\Excel', exist_ok=True)
    os.makedirs(r'Documents\Txt', exist_ok=True)
    os.makedirs(r'Documents\Others', exist_ok=True)
        
    try:
        os.mkdir('Miscs')
    except FileExistsError:
        logger.warning("Folder Miscs already exist.")

def _move_file(src: str, dst_folder: str):
    filename = os.path.basename(src)

    destination = _unique_path(
        os.path.join(dst_folder, filename)
    )

    shutil.move(src, destination)

def _move_files(DIR, files, folder):
    moved = 0

    for item in files:
        try:
            _move_file(
                os.path.join(DIR, item),
                os.path.join(DIR, "Documents", folder)
            )
            moved += 1

        except (PermissionError, FileNotFoundError):
            logger.error(
                f"{item} not found or moved, or not enough permission."
            )

    return moved
             
def sort_main(DIR: str) -> dict[str, Any]:
    (
        imgs,
        vids,
        docs,
        word_doc,
        txt_doc,
        ppt_doc,
        excel_doc,
        pdf_doc,
        miscs,
        other_doc,
        archives,
        executables,
        codes,
        audios,
    ) = classify_files()

    stats = {
        "images": 0,
        "videos": 0,
        "audios": 0,
        "archives": 0,
        "executables": 0,
        "codes": 0,
        "documents": 0,
        "others": 0,
    }

    def move_category(files, folder, key):
        moved = 0

        if not files:
            return 0

        for file in files:
            try:
                _move_file(
                    os.path.join(DIR, file),
                    os.path.join(DIR, folder),
                )
                moved += 1

            except (PermissionError, FileNotFoundError, shutil.Error):
                logger.error(f"{file} not found or could not be moved.")

        logger.info(f"Moved {moved} {key}.")
        return moved

    stats["images"] = move_category(imgs, "Images", "images")
    stats["videos"] = move_category(vids, "Videos", "videos")
    stats["audios"] = move_category(audios, "Audios", "audios")
    stats["archives"] = move_category(archives, "Archives", "archives")
    stats["executables"] = move_category(executables, "Executables", "executables")
    stats["codes"] = move_category(codes, "Codes", "codes")
    stats["others"] = move_category(miscs, "Miscs", "misc files")

    stats["documents"] = (
        _move_files(DIR, word_doc, "Word")
        + _move_files(DIR, pdf_doc, "PDF")
        + _move_files(DIR, excel_doc, "Excel")
        + _move_files(DIR, ppt_doc, "PPT")
        + _move_files(DIR, txt_doc, "Txt")
        + _move_files(DIR, other_doc, "Others")
    )

    logger.info(f"Moved {stats['documents']} documents.")

    total_files = (
        len(imgs)
        + len(vids)
        + len(audios)
        + len(archives)
        + len(executables)
        + len(codes)
        + len(miscs)
        + len(docs)
    )

    successfully_moved = sum(stats.values())
    errors = total_files - successfully_moved

    return {
    "total": total_files,
    "moved": successfully_moved,
    "failed": errors,
    "breakdown": stats,
}