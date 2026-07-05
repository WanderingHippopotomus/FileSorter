# File Sorter

A command-line Python application that automatically organizes files into categorized folders.

## Features

-  Sorts images into `Images/`
-  Sorts documents into `Documents/`
-  Sorts videos into `Videos/`
-  Sorts remaining files into `Miscs/`
-  Logs every operation
-  Measures total execution time
-  Handles common filesystem errors gracefully

## Technologies Used

- Python 3
- os
- shutil
- logging
- re
- time

## Project Structure

```
FileSorter/
│
├── main.py
│
└── backend/
    ├── classifier.py
    ├── sorter.py
    ├── logger.py
    │
    └── utils/
        ├── config.py
        └── time.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/FileSorter.git
```

Move into the project:

```bash
cd FileSorter
```

Run:

```bash
python main.py
```

## Example

```
======================================== 

                File Sorter!
-By WanderingHippopotomus
========================================
Enter location to sort (Default = Downloads): 

Total files moved: 441
Total time taken: 0.28s
Failed to move: 0
```

## Future Improvements

- Use `pathlib` instead of `os`
- Support additional file types
- Recursive folder sorting
- Duplicate file handling
- Configuration via JSON
- Automated folder monitoring

## Author

Kushagra Shrivastava
(WanderingHippopotomus)