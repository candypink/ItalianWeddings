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


class MyGUI:

    def __init__(self, master, df, out_name):

        # data-frame related
        self.df = df
        self.current_index = 0 # row index in df
        self.out_name = out_name # where to write df with sentiments
        self.total_processed = 0

        # logger        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SentimentAnalysis')

        # GUI
        self.master = master
        self.master.title('Sentiment analysis')
        # message text
        self.text = tk.Text(master, height=10, width=60,
                       font=("Arial", 18), wrap=tk.WORD)
        self.update_text()
        self.text.pack()        

        # buttons for answer
        tk.Button(self.master, text='Positive', highlightbackground='green',  
                  font=("Helvetica", 20),command = lambda: self.set_sentiment(1)).pack(side = tk.LEFT)
        tk.Button(self.master, text='Negative', highlightbackground='red',  
                  font=("Helvetica", 20),command = lambda: self.set_sentiment(2)).pack(side = tk.LEFT)
        tk.Button(self.master, text='Neutral', highlightbackground='blue',  
                  font=("Helvetica", 20),command = lambda: self.set_sentiment(3)).pack(side = tk.LEFT)
        tk.Button(self.master, text='Asking', highlightbackground='yellow',  
                  font=("Helvetica", 20),command = lambda: self.set_sentiment(0)).pack(side = tk.LEFT)
        tk.Button(self.master, text='EXIT', highlightbackground='grey',  
                  font=("Helvetica", 20),command = self.stop).pack(side = tk.LEFT)

    def set_sentiment(self, val):
        # set the value in the dataframe
        self.df.loc[self.current_index, 'sentiment'] = val
        # prepare for next sentence
        self.current_index +=1
        self.update_text()
        # update counter
        self.total_processed += 1

    def update_text(self):
        self.text.delete('1.0', tk.END)        
        title = str(self.df.iloc[self.current_index]['title'])
        message =  str(self.df.iloc[self.current_index]['text'])
        self.text.insert(tk.INSERT, "Title: ","bold")
        self.text.insert(tk.INSERT, title+'\n')
        self.text.insert(tk.INSERT, "Message:\n","bold")
        self.text.insert(tk.INSERT, message+'\n')
        self.text.tag_add("start", "1.0", "1.6")
        self.text.tag_add("start", "2.0", "2.7")
        self.text.tag_config("start", background="white", foreground="#485161", font=("Helvetica", "20", "bold"))



    def stop(self):
        self.logger.info(f'Poocessed: {self.total_processed}')
        self.logger.info(f'Writing dataframe in {self.out_name}')
        df.to_csv(self.out_name)
        self.logger.info('Leaving')
        self.master.destroy()

if __name__ == '__main__': 
    
    # parser for command-line arguments
    parser=argparse.ArgumentParser("Interactiveely classify messages as 'Asking', 'Positive', 'Negative', 'Neutral'", 
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', dest='input', type=str, default = '../results/forum_training.csv',  help='Input csv')
    parser.add_argument('-o', '--output', dest='output', type=str, help='Output csv')
    parser.add_argument('-r', '--replace', dest='replace', action='store_true',  help='Replace original input file')
    args=parser.parse_args()

    # read 
    df = pd.read_csv(args.input)
    # decide name of output file
    if args.replace:
        output_name = args.input
    elif args.output:
        output_name = args.output
    else:
        output_name = args.input.replace('.csv','_sentiment.csv')
        
    # loop with GUI
    top = tk.Tk()
    my_gui = MyGUI(top, df, output_name)
    top.mainloop()


