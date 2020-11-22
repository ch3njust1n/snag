import os
import requests
import pandas as pd
from pystagram import Instagram
from pytube import YouTube, Playlist
from tqdm import tqdm
from colorama import Fore, Style

'''
inputs:
url       (str)           URL to video
dst       (str)           Download directory
title     (str)           File name
extension (str, optional) File extension. Default: mp4

outputs:
out_file (str) Absolute path to saved file
'''
def download_stream(url, dst, title, extension):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        out_file = os.path.join(dst, f'{title}.{extension}')
        with open(out_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

            return out_file

'''
inputs:
link         (str)           URL to video
dst          (str)           Download directory
name         (str)           User given name of video
quality      (str, optional) Video quality
extension    (str, optional) Video extension type

outputs:
title     (str) Video title or link if successful
save_path (str) Absolute path to saved file
'''
def download(link, dst, name, quality='medium', extension='mp4'):
    title = ''
    qualities = {'tiny', 'small', 'medium', 'large', 'hd720', 'hd1080'}
    
    if not quality in qualities:
        raise Exception(f'Invalid quality given: {quality}')

    if 'youtube' in link:
        if 'playlist' in link: 
            try:
                Playlist(link).download_all(dst)
            except:
                return title, ''
        else:
            link = link.split('&')[0]
            try:
                yt = YouTube(link)
                stream = yt.streams.get_highest_resolution()
                video_streams = stream.player_config_args['url_encoded_fmt_stream_map']

                for vid in video_streams:
                    ext = vid['type'].split(';')[0].split('/')[-1]

                    if ext == extension and vid['quality'] == quality:
                        save_path = download_stream(vid['url'], dst, yt.title, extension)
                        return yt.title, save_path

            except Exception as e:
                print(e)
                return title, ''

    elif 'instagram' in link:
        if len(name) == 0:
            raise Exception(f'{Fore.RED}failed{Style.RESET_ALL} Filename required for Instagram videos')
            
        try:
            gram = Instagram(link)
            gram.download(dst=dst, filename=name)  
            title = link if len(name) == 0 else name
        except:
            return title

    else:
        raise Exception('snag api only supports YouTube and Instagram videos')

    return title

'''
inputs
file (list) List of string urls
dst  (str)  Absolute path to save directory

outputs:
errors (list) List of videos that could not be downloaded
'''
def download_list(file, dst):
    errors, successes = [], 0

    if file.endswith('.txt'):
        with open(file, 'r') as f:
            for line in tqdm(f.readlines()):
                line = line.strip()
                name = line.split('/p/')[-1].split('/')[0]
                try:
                    download(line, dst, name)
                    successes += 1
                except Exception as e:
                    errors.append(line)

    elif file.endswith('.tsv'):
        df = pd.read_csv(file, header=0, sep='\t')

        for i, row in df.iterrows():
            if isinstance(row['link'], str) and len(row['link']) > 0:
                save = row['channel']+'-'+row['embed'] if row['embed'] is None else row['channel']
                download(row['link'], dst, save)
            else:
                errors.append(list(row))

    return errors, successes