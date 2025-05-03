## Process ##
First, I downloaded the T06 files from [this](https://drive.google.com/drive/folders/1yD3q2JKhFl4cDPFOrHH4Q8S2AIsAwrxJ) google drive.  Then I looked at the CSVs to determine the common "time" variable, that ended up being "True frame #".  I then ran the data_compare.py script using the following input:
```bash
python data_compare.py .\Peg_Transfer_S01_T06_trakStar_final.csv .\Peg_Transfer_S01_T06.csv T06 "True frame #" 1.0 0.0 False
```
and got the following images:
![trakStar data](./images/T06_file1.png)
TrakStar Data
![raven data](./images/T06_file2.png)
Raven Data
![combined data](./images/T06_merged.png)
Combined Data
## Comparison ##

Without any manipulation, I was able to find the following variables that corresponded by visually comparing the graphs
| TrakStar| Raven      |
|:--------|----------------:|
|PSML_position_x | PSML_position_x|
|PSML_position_y | PSML_position_y|
|PSML_positoin_z | PSML_position_z|
|PSMR_position_x | PSMR_position_x|
|PSMR_position_y | PSMR_position_y|
|PSMR_positoin_z | PSMR_position_z|
|PSML_gripper_angle | PSML_gripper_angle|
|PSMR_gripper_angle | PSMR_gripper_angle|

The raven data also had velocity data for each grip (at least I am assuming PSMR/PSML are the grips of the robot).

I also plotted the common columns with eachother on plots and they are nearly identical as seen in the image.
![overlapping data](./images/T06_overlap.png)
