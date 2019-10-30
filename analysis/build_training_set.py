import numpy as np 
import pandas as pd
from datetime import datetime
import argparse
import logging
import time

if __name__ == '__main__': 
    
    # parser for command-line arguments
    parser=argparse.ArgumentParser("Interactiveely classify messages as 'Asking', 'Positive', 'Negative', 'Neutral'", 
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', dest='input', type=str, default = '../results/forum_training.csv',  help='Input csv')
    parser.add_argument('-o', '--output', dest='output', type=str, help='Output csv')
    parser.add_argument('-r', '--replace', dest='replace', action='store_true',  help='Replace original input file')
    args=parser.parse_args()

    # logging config
    logging.basicConfig(level=logging.INFO)

    # read 
    logging.info(f'Reading {args.input}')
    df = pd.read_csv(args.input)
    # decide name of output file
    output_created = False
    if args.replace:
        output_name = args.input
    elif args.output:
        output_name = args.output
    else:
        output_name = args.input.replace('.csv','_sentiment.csv')
    # loop each row
    for index, row in df.iterrows():
        if row['sentiment'] != -99:
            continue
        print('Message:')
        print(row['title'],'\n',row['text'])
        try:
            sentiment = input('Type category and press enter \n[ Asking:0, Positive:1, Negative:2, Neutral:3 ] \nCTRL-C to stop \n')
        # allow stopping with CRTL-C
        except KeyboardInterrupt:
            df.to_csv(output_name)
            output_created = True
            break
        if sentiment not in ['0','1','2','3']:
            logging.warning('Setting sentiment to neutral')
            sentiment = 3
        df.at[index,'sentiment'] = sentiment
        time.sleep(0.33)

    if not  output_created:
        df.to_csv(output_name)

