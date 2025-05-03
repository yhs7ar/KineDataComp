### Conclusions ###

## Process ##
First I downloaded the T06 files from [this](https://drive.google.com/drive/folders/1yD3q2JKhFl4cDPFOrHH4Q8S2AIsAwrxJ) google drive.  Then I looked at the CSVs to determine the common "time" variable, that ended up being "True frame #".  I then ran the data_compare.py script using the following input:
```bash
python data_compare.py .\Peg_Transfer_S01_T06_trakStar_final.csv .\Peg_Transfer_S01_T06.csv T06 "True frame #" 1.0 0.0 False
```
and got the following images:
