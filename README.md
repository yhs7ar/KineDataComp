# KineDataComp
Comparison of Kinematics from Raven Surgical Robot and TrakStar Motion Tracking System

This is a python script that takes two input CSV files and creates stacked tables for each column against time, it also will sync any unsynced data and scale resolution to match the resolution of the lower resolution file.

# Dependencies Required
Python 3.12.10 or later.  Download instructions [Here](https://wiki.python.org/moin/BeginnersGuide/Download).\
pandas Library. Download instructions [Here](https://pandas.pydata.org/docs/getting_started/install.html).\
cv2 Library. Download instructions [Here](https://docs.opencv.org/4.x/d5/de5/tutorial_py_setup_in_windows.html).\
matplotlib Library. Download instructions [Here](https://matplotlib.org/stable/install/index.html).

# How to use
Download the data_compare.py file and then in powershell navagate to its directory (if you download it to your downloads folder on a windows machine you can use the command, make sure to change %USERNAME% to your windows username):
```bash
cd C:\Users\%USERNAME%\Downloads
```
Then you type 
```bash
python data_compare.py
```
and it will output an example of usage and the inputs, change your inputs accordingly and the file will create a png of your graphs to be used for analysis.  If you want to exclude certain columns, you have to change your CSV file so that it no longer includes those columns.  You also want to make sure you chose the proper column for the time column between the two files.
