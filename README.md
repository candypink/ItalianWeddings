# WIP: Trends for Italian weddings

Look into the forum of the popular Italian wedding website [matrimonio.com](http://www.matrimonio.com) 
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


