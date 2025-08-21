# DeadScan

## Overview
**DeadScan** is a fast, multi-threaded and riliable port scanning tool written in Python. This Tool allows you to scan for open ports on a target IP address or domain, specify the range of ports to scan, and control the number of concurrent threads to speed up the process, Scan TCP or UDP, Runs riliability scans in background, etc.

## Features
- Fast, multi-threaded scanning using Python's threading module.
- Options to Scan UDP or TCP Ports.
- run riliability scans in background for accurate results.
- Customizable port ranges.
- Option to display the time taken to complete the scan.
- Simple and lightweight, with minimal dependencies.

## Prerequisites
- Python 3.x
- Required Python packages:
  - `socket`
  - `threading`
  - `argparse`
  - `rich`

You can install the necessary packages using pip:
```sh
pip install socket threading argparse rich
```

## Usage

  - Run the script:

    ```sh
    python3 DeadScan.py -h
    ```
  - To use DeadScan, run the following command:
    ```sh
    python3 deadscan.py -i <target-ip> [-sp <start-port>] [-ep <end-port>]
    ```
  

## Conclusion

The **DeadScan Tool** is efficiant way to scan port on a host.

Feel free to contribute or suggest improvements by opening an issue or submitting a pull request. Enjoy Using it...
