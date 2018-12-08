# torrentphile
bittorrent clone and a wordplay on file and phile. 

# contributors
@ashleytqy
@tommyguo

# what
A P2P file transfer application similar to BitTorrent – where a user can upload any file, which will be distributed across the other users online in the system. When a user wants to retrieve a specific file, they will get the various pieces of the file from the other online users.

# assumptions
- All users stay online during throughout the uploading / downloading of the files (no partitions)
- All users are "friendly" (no malicious attacks against our tracker, it seeds files that it has downloaded indefinitely).
- All parts of the original file exists within the system (no need for replication)

# interface

## setting up
```
# for the tracker
p2p start

# for the clients
p2p register [port number]
```
## uploading
```
p2p upload [filename]
```

## downloading
```
p2p download [file url]
```

# references
http://www.bittorrent.org/bittorrentecon.pdf
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.114.4974&rep=rep1&type=pdf
