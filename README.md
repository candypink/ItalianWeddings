# WIP: Trends for Italian weddings

While organising my own wedding, I often wondered what other brides whould have thought about my choice 
of decorations, entertainment, music and so on. To answer these questions, I am 
look into the forum of the popular Italian wedding website [matrimonio.com](http://www.matrimonio.com) 
to gain insight on trends related to weddings in Italy. 

![Scarpe](figures/scarpe.jpg)

## Getting the data

The data is obtained scraping the forum of [matrimonio.com](http://www.matrimonio.com)
The code of the spider is [here](matrimonio/spiders/forum.py), and to run it you just need to do: 


```bash
scrapy crawl forum -o my_results.csv
```

This will take quite some timee since the forum is very pupulated. 
It is also taking care of a first few steps of **data cleaning** (the things 
I am sure I want to be dene regardless of the subsequent analysis), 
in particular:
* all text is put in lower case and leading and trailling white spaces are 
removed
* the date format is changed from a string in italian to a numeric format

The output file contains the following information:
* `title`: title of the post or "comment" in case of comments to a post
* `text`: body of the message
* `id`: unique id of the message/comment
* `parent_id`: for comments id of the original message, for the initial message is the same as the `id`
* `author`: id of the author of the message/comment
* `time`: string with time in the format `'%Y-%m-%d %H:%M'`
