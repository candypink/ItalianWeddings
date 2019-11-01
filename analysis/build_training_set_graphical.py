#!/usr/local/bin/python3.7
'''
#!/usr/bin/python
'''
import numpy as np 
import pandas as pd
from datetime import datetime
import argparse
import logging
import time

import tkinter as tk # for the graphical interface

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
    #logging.info(f'Reading {args.input}')
    #logging.info(f'Reading ')
    df = pd.read_csv(args.input)
    # decide name of output file
    output_created = False
    if args.replace:
        output_name = args.input
    elif args.output:
        output_name = args.output
    else:
        output_name = args.input.replace('.csv','_sentiment.csv')
    counter_done = 0
    # loop each row
    for index, row in df.iterrows():
        if row['sentiment'] != -99:
            continue

        sentiment = -99
        def set_value(value):
            global sentiment
            sentiment = value
            top.destroy()            
        top = tk.Tk()
        pane = tk.Frame(top)
        pane.pack(fill = tk.BOTH, expand = True) 
        text = tk.Text(pane, height=10, width=40,
                       font=("Helvetica", 20))
        text.insert(tk.INSERT, row['title'],'\n',row['text'])
        text.pack()
        
        Pos = tk.Button(pane, text ="Positive", 
                        highlightbackground = "green",
                        font=("Helvetica", 20), 
                        command = lambda *args: set_value(1)
                        )
        Neg = tk.Button(pane, text ="Negative", 
                        highlightbackground = "red", 
                        font=("Helvetica", 20), 
                        command = lambda *args: set_value(2) )
        Neu = tk.Button(pane, text ="Neutral", 
                        highlightbackground = "blue",  
                        font=("Helvetica", 20),
                        command = lambda *args: set_value(3) )
        Ask = tk.Button(pane, text ="Asking", 
                        highlightbackground = "yellow", 
                        font=("Helvetica", 20), 
                        command = lambda *args: set_value(0) )

        
        Pos.pack(side = tk.LEFT)
        Neg.pack(side = tk.LEFT)
        Neu.pack(side = tk.LEFT)
        Ask.pack(side = tk.LEFT)
        
        top.mainloop()
        print(f'Sentiment {sentiment}')
        if sentiment not in [0,1,2,3]:
            logging.warning('Setting sentiment to neutral')
            sentiment = 3
        df.at[index,'sentiment'] = sentiment
        counter_done += 1
        time.sleep(0.33)

    if not  output_created:
        df.to_csv(output_name)

