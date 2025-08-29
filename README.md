# Privacy Guard Pro

Privacy Guard Pro is a command-line interface (CLI) application built with Python to help you inspect and scrub sensitive metadata from your files, particularly images.

Digital files often contain hidden Exif (Exchangeable Image File Format) data, which can include personal information like GPS coordinates, camera details, and timestamps. This tool provides an easy way to view and remove this data before sharing your files online.

[Here is a video giving details about the CLI](https://www.loom.com/share/3d85a419ecb44a85b5bebf43e38a4098?sid=4f951519-0f4a-4a66-8a20-40c7bbfbe5f4)

## Features

-   **Metadata Preview**: View all hidden metadata for a specific file.
-   **Complete & Selective Scrubbing**: Remove all metadata at once or choose specific tags to remove.
-   **Batch Processing**: Process a single file or an entire directory of files.
-   **Scrubbing Profiles**: Create, save, and reuse custom profiles with predefined lists of metadata tags to remove (e.g., a "Web Safe" profile that removes location and device info).
-   **Audit Trail**: All scrubbing operations are logged in an SQLite database, providing a complete history of processed files and removed data.

## Tech Stack

-   **Python**
-   **SQLAlchemy ORM**: For database interaction and modeling.
-   **Pillow (PIL Fork)**: For reading and manipulating image metadata.
-   **Rich**: For creating beautiful and informative CLI outputs.
-   **Pipenv**: For managing project dependencies and the virtual environment.

## Project Structure

```
privacy_guard_pro/
├── Pipfile
├── Pipfile.lock
├── README.md
├── cli.py
└── test_images
└── lib/
    ├── __init__.py
    ├── db/
    │   ├── __init__.py
    │   ├── database.py
    │   └── models.py
    ├── helpers.py
    └── scrubber.py
```

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd privacy_guard_pro
    ```

2.  **Install dependencies using Pipenv:**
    Make sure you have Pipenv installed (`pip install pipenv`).
    ```bash
    pipenv install
    ```

3.  **Activate the virtual environment:**
    ```bash
    pipenv shell
    ```

## How to Run

Once inside the Pipenv shell, run the main CLI application:

```bash
python cli.py
```

You will be greeted with the main menu where you can choose to scrub files, manage profiles, or view the audit trail.

---

## Author
• Daniel Muhia

## License
MIT License
Copyright (c) 2025 Privacy Guard Pro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
