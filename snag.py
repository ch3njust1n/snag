import os
import sys
import argparse
import pandas as pd
from colorama import Fore, Style
from pystagram import Instagram
from pytube import YouTube, Playlist
from tqdm import tqdm
from datetime import datetime



def download(link, dst, name, print_status=True):
    if 'youtube' in link:
        if 'playlist' in link: Playlist(link).download_all(dst)
        else:
            link = link.split('&')[0]
            yt = YouTube(link)
            yt.streams.get_highest_resolution().download(dst)
            if print_status: print(f'{Fore.GREEN}downloaded{Style.RESET_ALL} {yt.title}')
    elif 'instagram' in link:
        if len(name) == 0:
            raise Exception(f'{Fore.RED}failed{Style.RESET_ALL} Filename required for Instagram videos')
            
        gram = Instagram(link)
        gram.download(dst=dst, filename=name)
        if print_status: print(f'{Fore.GREEN}downloaded{Style.RESET_ALL} {link if len(name) == 0 else name}')


def download_list(file, dst):
    errors = []
    if file.endswith('.txt'):
        with open(file, 'r') as f:
            for line in tqdm(f.readlines()):
                line = line.strip()
                name = line.split('/p/')[-1].split('/')[0]
                try:
                    download(line, dst, name, print_status=False)
                except Exception as e:
                    errors.append(line)
    elif file.endswith('.tsv'):
        df = pd.read_csv(file, header=0, sep='\t')

        for i, row in df.iterrows():
            if isinstance(row['link'], str) and len(row['link']) > 0:
                save = row['channel']+'-'+row['embed'] if row['embed'] is None else row['channel']
                download(row['link'], dst, save)
            else:
                print(f'{Fore.RED}{list(row)}')

    print(f'{Fore.RED}{len(errors)} failed{Style.RESET_ALL}')
    for url in errors:
        print(url)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--link', '-l', type=str, help='YouTube or Instagram link. (required)')
    parser.add_argument('--name', '-n', type=str, default='', help='File name. Required for Instagram videos.')
    parser.add_argument('--dst', '-d', type=str, default=os.path.expanduser('~/Downloads'), help='Save destination (default: downloads)')
    parser.add_argument('--file', '-f', type=str, help='File of urls to download')
    
    args = None

    try:
        args = parser.parse_args()
    except:
        raise Exception(f'{Fore.RED}failed{Style.RESET_ALL} could not parse arguments')

    if args.link is None and args.file is None:
        raise Exception(f'{Fore.RED}error:{Style.RESET_ALL} Must set either -link or -file options')

    if not os.path.exists(args.dst): 
        os.makedirs(args.dst)

    if args.file is None: 
        download(args.link, args.dst, args.name)
    else:
        download_list(args.file, args.dst)


if __name__ == '__main__':
    main()
