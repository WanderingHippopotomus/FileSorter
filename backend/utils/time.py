# Built by WanderingHippopotomus

import time

def time_to_run(func, *args) -> float:
    start = time.perf_counter()
    details = func(*args)
    end = time.perf_counter()
    
    runtime = f'{end - start:.2f}s'
    
    return runtime, details