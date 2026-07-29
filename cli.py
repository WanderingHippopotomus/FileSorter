# Built by WanderingHippopotomus

from backend.sorter import sort_main, create_dir
from backend.utils.time import time_to_run
from backend.logger import logger
import os

def main():
    print('='*40,'\n\n\t\tFile Sorter!\n-By WanderingHippopotomus\n','='*40)
    
    directory = input("Enter location to sort (Default = Downloads): \n").strip()
    
    DIR = directory or r'C:\Users\HP\Downloads'
    
    logger.info(f"Current directory is {DIR}")
    
    os.chdir(DIR)
    
    create_dir()
    
    run_time = time_to_run(lambda: sort_main(DIR))
    
    print(f"Total files moved: {run_time[1][1]}\nTotal time taken: {run_time[0]}\nFailed to move: {run_time[1][2]}")
    logger.info(f"Total files moved: {run_time[1][1]}\nTotal time taken: {run_time[0]}")
    logger.error(f"Failed to move: {run_time[1][2]}")
    
if __name__ == '__main__':
    main()    