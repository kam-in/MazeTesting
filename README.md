# Design Tests [notes for April]

This is a reduced set of codes for the purpose of testing new maze designs 
- removed demo, practice, block repetition, etc. to allow for simply loading/testing the maze designs

1. Txt files with maze designs are in this directory: block1 
  The code loads and goes through all txt files in this directory. 
  For now, I've only put one (AprilNew2.txt: the maze #2 in our design spreadsheet    (https://docs.google.com/spreadsheets/d/1E5mf8nWh6n2AFcmjj3vgF_wFdkPGytdiiczdROdz4Vc/edit#gid=0))

2. To test other designs, create and add txt files that contain the designs in this directory. 
   Feel free to be creative with naming your mazes!! Clearly I was not very creative with that. :-/

3. If you want to check navigation results, data files are saved in directory: solving_log_dir 

4. In case you want to test larger revealing (2 steps, 3 steps, etc.), change the initial level in the code updateVisible.m 
  Specifically, in line 22, it starts from 1 (levels = 1: -1: 1). If you make it levels (3:-1:1), it will reveal 3 square-range from the agent's location. 


 
   
