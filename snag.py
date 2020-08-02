import os
import sys
import argparse
import pandas as pd
from colorama import Fore, Style
from pystagram import Instagram
from pytube import YouTube, Playlist


def download(link, dst, name):
    if 'youtube' in link:
        if 'playlist' in link: Playlist(link).download_all(dst)
        else:
            yt = YouTube(link)
            yt.streams.get_highest_resolution().download(dst)
            print(f'downloaded {yt.title}')
    elif 'instagram' in link:
        if len(name) == 0:
            raise Exception('Filename required for Instagram videos')
            
        gram = Instagram(link)
        gram.download(dst=dst, filename=name)
        print(f'{Fore.GREEN}downloaded{Style.RESET_ALL} {link if len(name) == 0 else name}')


def download_list(file, dst):
    if file.endswith('.txt'):
        with open(file, 'r') as f:
            for line in f.readlines():
                download(line.strip(), dst, name)
    elif file.endswith('.tsv'):
        df = pd.read_csv(file, header=0, sep='\t')

        for i, row in df.iterrows():
            if isinstance(row['link'], str) and len(row['link']) > 0:
                save = row['channel']+'-'+row['embed'] if row['embed'] is None else row['channel']
                download(row['link'], dst, save)
            else:
                print(f'{Fore.RED}{list(row)}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--link', '-l', type=str, required=True, help='YouTube or Instagram link. (required)')
    parser.add_argument('--name', '-n', type=str, default='', help='File name. Required for Instagram videos.')
    parser.add_argument('--dst', '-d', type=str, default='downloads', help='Save destination (default: downloads)')
    parser.add_argument('--file', '-f', type=str, help='File of urls to download')
    args = parser.parse_args()

    if not os.path.exists(args.dst): 
        os.makedirs(args.dst)

    if args.file is None: 
        download(args.link, args.dst, args.name)
    else:
        download_list(args.file, args.dst)


if __name__ == '__main__':
    main()
