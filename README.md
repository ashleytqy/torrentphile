# Torrentphile
bittorrent clone and a wordplay on file and phile. 

# Contributors
@ashleytqy
@tommyguo

# What
A P2P file transfer application similar to BitTorrent – where a user can upload any file, which will be distributed across the other users online in the system. When a user wants to retrieve a specific file, they will get the various pieces of the file from the other online users.

# Assumptions
- All users stay online during throughout the uploading / downloading of the files (no partitions)
- All users are "friendly" (no malicious attacks against our tracker, it seeds files that it has downloaded indefinitely).
- All parts of the original file exists within the system (no need for replication)
- We won't be using a persistent database like MySQL etc. to keep things simple
- Contents of files with the same name are the same, i.e. File1.txt === File2.txt
- Each client has a specific folder where it stores it's downlaoded file / file chunks, in `/tmp/client_id`
- The downloaded file chunks of file `test.txt` lives in `/tmp/client_id/test/1...10.txt`

# Upload
During the upload process, Client A talks to the Tracker and notifies the Tracker that A has a certain file. Client A then splits the file into smaller chunks.

# Download


# References
http://www.bittorrent.org/bittorrentecon.pdf
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.114.4974&rep=rep1&type=pdf
