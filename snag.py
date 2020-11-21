import os
import sys
import argparse
from colorama import Fore, Style
from api.video import download_list, download


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--link', '-l', type=str, help='YouTube or Instagram link. (required)')
    parser.add_argument('--name', '-n', type=str, default='', help='File name. Required for Instagram videos.')
    parser.add_argument('--dst', '-d', type=str, default=os.path.expanduser('~/Downloads'), help='Save destination (default: downloads)')
    parser.add_argument('--file', '-f', type=str, help='File of urls to download')
    parser.add_argument('--quality', '-q', type=str, default='medium' help='Video quality (default: medium)')
    parser.add_argument('--extension', '-e', type=str, default='mp4' help='Video extension (default: mp4)')
    
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
        title = download(args.link, args.dst, args.name, args.quality, args.extension)

        if len(title) > 0:
            print(f'{Fore.GREEN}downloaded{Style.RESET_ALL} {title}')
        else:
            print(f'{Fore.RED}1{Style.RESET_ALL} failed {args.link}')
    else:
        errors, successes = download_list(args.file, args.dst)
        
        if len(errors) > 0:
            for url in errors:
                print(url)
            
            print(f'{Fore.RED}{len(errors)}{Style.RESET_ALL} errors')
        
        print(f'{Fore.GREEN}{successes}{Style.RESET_ALL} downloaded')
            

if __name__ == '__main__':
    main()
