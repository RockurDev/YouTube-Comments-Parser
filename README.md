# YouTube Comments Collector

This project provides two versions of a YouTube comments collectors implemented in Python: one using asynchronous programming (`main_async.py`) and the other using synchronous programming (`main_sync.py`). The scripts fetch comments from YouTube videos specified in `links.txt`, clean and store them in separate text files.

## Comparison of Synchronous and Asynchronous Versions

- **Asynchronous Version (`main_async.py`):**
  - Utilizes `httpx.AsyncClient` for asynchronous HTTP requests.
  - Efficiently handles multiple concurrent requests, suitable for I/O-bound operations.
  - Ideal for scenarios requiring scalability and responsiveness under load.

- **Synchronous Version (`main_sync.py`):**
  - Uses `httpx.Client` for synchronous HTTP requests.
  - Executes requests sequentially, blocking until each request completes.
  - Simpler to understand and implement, suitable for smaller scale operations or when synchronous behavior is preferred.

## Getting Started

To use either version of the collector, ensure you have Python installed on your system along with the necessary dependencies listed in `requirements.txt`.

### Prerequisites

- Python 3.7+
- `httpx` library (automatically installed via `requirements.txt`)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/RockurDev/YouTube-Comments-Collector.git
   cd YouTube-Comments-Collector
   ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
### Usage
Asynchronous (main_async.py) and synchronous (main_sync.py) versions work identically:

1. Place YouTube video URLs in links.txt (one URL per line).

2. Execute the script:
    Asynchronous version
    ```bash
    python main_async.py
    ```
    Synchronous version
    ```bash
    python main_async.py
    ```
3. Output:
    Cleaned comments are stored in data_sync/comments_{video_id}.txt.

### File Structure
- `main_async.py`: Asynchronous version of the YouTube comments collector.
- `main_sync.py`: Synchronous version of the YouTube comments collector.
- `links.txt`: File where users paste YouTube video URLs for parsing.
- `data_async/`: Directory where cleaned comments are stored (for async version).
- `data_sync/`: Directory where cleaned comments are stored (for sync version).
- `requirements.txt`: List of Python packages required for the project.
