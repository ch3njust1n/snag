# snag
Snag videos from Instagram and YouTube with Pystagram and Pytube

### Setup
`$ sh setup.sh`

### Usage
```
--link -l YouTube or Instagram link. (required)
--name -n File name. Required for Instagram videos.
--dst  -d Save destination (default: queue)
--file -f File of urls to download
```

### Example

#### Single video
```
$ python snag.py -l https://www.youtube.com/watch?v=QlsaQZz6418
```

#### Youtube playlist
```
$ python snag.py -l https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU
```

#### Instagram video
```
$ python snag.py -l https://www.instagram.com/p/BuEelMGnYpW/ -n dope
```

#### File of urls
Supports `.txt` and `.tsv`. Label tsv column as `link` and place file inside project folder.
```
$ python snag.py -f videos.tsv
```

