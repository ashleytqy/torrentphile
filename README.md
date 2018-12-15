# Torrentphile
bittorrent clone and a wordplay on file and phile. 

# Contributors
@ashleytqy
@tommyguo

# What
A peer-to-peer file transfer application similar to BitTorrent where users can upload files that will be distributed across the other users online in the system when they download the file, as opposed to a central server storing all the files.

# Assumptions
- All users stay online during throughout the uploading / downloading of the files (no partitions)
- All users are "friendly" (no malicious attacks against our tracker, it seeds files that it has downloaded indefinitely).
- We won't be using a persistent database like MySQL etc. to keep things simple
- Contents of files with the same name are the same, i.e. `sha1(file1.txt) === sha1(file1.txt)`
- Each client has a specific folder where it stores the files it currently have, and files that it will be downloading, in `/tmp/client_id`
- We're only supporting `.txt` files for simplicity
- We won't be splitting the files into multiple chunks and distributing the chunks across multiple peers. Instead, we will be sending the whole file for simplicity

---
# Set Up
- The Tracker server is set up to listen on port 8000
- 5 client servers are initialised and registers itself with the Tracker
- The Tracker sends an `ACK` to the client if the registration succeeds
- The Tracker continually listen on a port for any incoming client requests to upload or download a file

# Upload Process
- Client A wants to upload `test.txt`
- It informs the Tracker that it has `test.txt` and the Tracker updates it's internal records of which clients have which files
- Tracker sends an `ACK` to the client

# Download Process
- Client B wants to download `test.txt`
- It asks the Tracker which peers have `test.txt`
- The Tracker randomly chooses a peer from it's internal records, Peer C
- Client B makes a connection with Peer C to download `test.txt`
- Peer C sends `test.txt` to Client B and `test.txt` ends up in Client B's local directory

---
# Running
```
python3 simulator.py
```
This sets up the environment by creating folders for each client in `/tmp`, i.e. `/tmp/10000`, `/tmp/10001`... and creating the test files for a client. Then, it simulates client uploads and downloads.

After running the simulation, the `/tmp` directory should look like this:
```
├── 10000
│   ├── test1.txt
│   └── test3.txt
├── 10001
├── 10002
│   └── test1.txt
├── 10003
│   └── test3.txt
├── 10004
│   ├── test1.txt
│   └── test3.txt
```

# References
- https://cs.nyu.edu/courses/fall18/CSCI-UA.0480-009/lectures/lec18.pdf
- http://www.bittorrent.org/bittorrentecon.pdf
- http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.114.4974&rep=rep1&type=pdf
