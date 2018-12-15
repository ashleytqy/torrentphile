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
- Contents of files with the same name are the same, i.e. sha1(file1.txt) === sha1(file2.txt)
- Each client has a specific folder where it stores the files it currently have, and files that it will be downloading, in `/tmp/client_id`
- We're only supporting `.txt` files for simplicity
- We won't be splitting the files into multiple chunks and distributing the chunks across multiple peers. Instead, we will be sending the whole file for simplicity

# Upload
- Client A wants to upload `test.txt`
- It informs the Tracker that it has `test.txt` and the Tracker updates it's internal records of which clients have which files
- Tracker sends an `ACK` to the client

# Download
- Client B wants to download `test.txt`
- It asks the Tracker which peers have `test.txt`
- The Tracker randomly chooses a peer from it's internal records, Peer C
- Client B makes a connection with Peer C to download `test.txt`
- Peer C sends `test.txt` to Client B and `test.txt` ends up in Client B's local directory

# References
http://www.bittorrent.org/bittorrentecon.pdf
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.114.4974&rep=rep1&type=pdf
