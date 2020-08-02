import os
import sys
import argparse
from pystagram import Instagram
from pytube import YouTube, Playlist


def download_video(url, dst):
    yt = YouTube(url)
    yt.streams.get_highest_resolution().download(dst)
    print(f'downloaded {yt.title}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--link', '-l', type=str, required=True, help='YouTube or Instagram link. (required)')
    parser.add_argument('--name', '-n', type=str, default='', help='File name. Required for Instagram videos.')
    parser.add_argument('--dst', '-d', type=str, default='downloads', help='Save destination (default: downloads)')
    args = parser.parse_args()

    if not os.path.exists(args.dst): 
        os.makedirs(args.dst)

    if 'youtube' in args.link:
        if 'playlist' in args.link: Playlist(args.link).download_all(args.dst)
        else: download_video(args.link, args.dst)
    elif 'instagram' in args.link:
        if len(args.name) == 0:
            raise Exception('Filename required for Instagram videos')
            
        gram = Instagram(args.link)
        gram.download(dst=args.dst, filename=args.name)
        print(f'downloaded {args.link if len(args.name) == 0 else args.name}')

if __name__ == '__main__':
    main()
