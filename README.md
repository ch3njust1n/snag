# snag
Snag videos from Instagram and YouTube with Pystagram and Pytube

### Setup
`sh setup.sh`

### Usage
```
--link -l YouTube or Instagram link. (required)
--name -n File name. Required for Instagram videos.
--dst  -d Save destination (default: queue)
```

### Example

#### Single video
```
$ python snap.py -l https://www.youtube.com/watch?v=QlsaQZz6418
```

#### Youtube playlist
```
$ python snap.py -l https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU
```

#### Instagram video
```
$ python snap.py -l https://www.instagram.com/p/BuEelMGnYpW/ -n dope
```
