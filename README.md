E6893 Big Data Analytics  
Columbia University  
12/22/2016  
Nan Zhao, Ben Zhu, Sabina Smajlaj  
Professor Chin-Yung Lin  

#    EoD Price Predictor

1. Data Source: 
      1. Twitter Dumps

            Full Archive: https://archive.org/details/twitterstream

            July, 2016: https://archive.org/details/archiveteam-twitter-stream-2016-07  

            June, 2016: https://archive.org/details/archiveteam-twitter-stream-2016-06 

            Auguest, 2016: https://archive.org/details/archiveteam-twitter-stream-2016-05

      2. Stock Price

            Quandl API: https://www.quandl.com/docs/api


2. Tools Used: 

      Python, Sk-learn, Hadoop, Pandas, Numpy, JSON, Regular Expression

3. User guide:

      1. Data Fetching
         get_rel_entries_bash and unzip_dir_bash are responsible for unzipping all data from different directories as well as sub directories. Each archive file is in form of Month-Day-Hour for subdirectories within the file. User shall run unzip_dir_bash and get_rel_entries_bash under Month folder to get 8 different csv for different company mentions.

      2. Data Parsing, Cleaning and ML model
        pivot_data.py, Quandl_data_parse.ipynb, Join_data_and_ML_model.ipynb
        These files are responsible for cleaning, arregating data from multiple csv files and generate ML models for servers to provide predictions.

      3. Web Hosting
        All source code is within web_server folder. LINK to web app: http://e6893stockmarketpredictor.herokuapp.com 
        Web is written in Python with Flask infrastructure. 
  
  
