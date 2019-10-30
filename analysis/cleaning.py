import numpy as np 
import pandas as pd
from datetime import datetime
import argparse
import logging

if __name__ == '__main__': 
    
    # parser for command-line arguments
    parser=argparse.ArgumentParser("Remove nan and add year, month, day", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', dest='input', type=str, default = '../results/forum.csv',  help='Input csv')
    parser.add_argument('-o', '--output', dest='output', type=str, help='Output csv')
    parser.add_argument('-t', '--training', dest='training', action='store_true',  help='Write training sample')
    parser.add_argument('-c', '--cleaning', dest='cleaning', action='store_true',  help='Clean and sort csv')
    parser.add_argument('--training-entries', dest='trainingEntries', type=int, default=5000, help='Number of entries in the training csv')
    args=parser.parse_args()

    # logging config
    logging.basicConfig(level=logging.INFO)

    # read 
    logging.info(f'Reading {args.input}')
    df = pd.read_csv(args.input)

    if args.cleaning:
        # make changes we need
        logging.info(f'Sorting {args.input}')
        df.sort_values(['parent_id', 'time'],  inplace=True)
        logging.info('Applying changes')
        df['text']=df['text'].fillna("")
        df['time'] = df['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M'))
        df['year'] = df['time'].apply(lambda x: x.year)
        df['month'] = df['time'].apply(lambda x: x.month)
        df['day'] = df['time'].apply(lambda x: x.day) 
        df['sentiment'] = -99

        # write
        if args.output:
            output_name = args.output
        else:
            output_name = args.input.replace('.csv', '_cleaning.csv')
        logging.info(f'Writing {output_name}')
        df.to_csv(output_name)

    # write training csv
    if args.training:
        training_name = args.input.replace('.csv', '_training.csv')
        not_training_name = args.input.replace('.csv', '_not_training.csv')
        frac_training = float(args.trainingEntries)/df.shape[0]
        if frac_training > 1: 
            frac_training = 1            
            logging.warining('Requesting more training events than total number of events')
        logging.info(f'Fraction of entries for training: {frac_training}')
        mask = np.random.rand(len(df)) < frac_training
        df_training = df[mask]
        df_not_training = df[~mask]
        logging.info(f'Writing {training_name}')
        df_training.to_csv(training_name)
        logging.info(f'Writing {not_training_name}')
        df_not_training.to_csv(not_training_name)

