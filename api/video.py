import pandas as pd
from pystagram import Instagram
from pytube import YouTube, Playlist
from tqdm import tqdm
from colorama import Fore, Style

'''
inputs:
link         (str) URL to video
dst          (str) Download directory
name         (str) User given name of video

outputs:
title (str) Video title or link if successful
'''
def download(link, dst, name):
    title = ''

    if 'youtube' in link:
        if 'playlist' in link: 
            try:
                Playlist(link).download_all(dst)
            except:
                pass
        else:
            link = link.split('&')[0]
            try:
                yt = YouTube(link)
                yt.streams.get_highest_resolution().download(dst)
                title = yt.title
            except:
                pass

    elif 'instagram' in link:
        if len(name) == 0:
            raise Exception(f'{Fore.RED}failed{Style.RESET_ALL} Filename required for Instagram videos')
            
        try:
            gram = Instagram(link)
            gram.download(dst=dst, filename=name)  
            title = link if len(name) == 0 else name
        except:
            pass

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