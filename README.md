# Fathom-Additional-System-Locator
Fathom additional system locator to determine which locations on a campus system chilled water hydraulic model will allow for connections of additional buildings based on new GPM load and allowed maximum velocity 


Required export outputs : Pipe #, Pipe Nominal Size,Vol. Flow Rate (gal/min), Velocity (feet/sec) as a .csv file. Resave the file after exporting from Fathom to remove any encoding issues with the .csv
The script will locate these from an AFT Fathom export (AFT Fathom 11)

Final output file will be placed into the same folder as .csv upload location

File will be saved as *filename*.*#gpm*


## Walkthrough:

1) Download contents in the folder.

2) Export an AFT Fathom .csv file making sure to export the required outputs:

![](https://github.com/zdiam/Fathom-Additional-System-Locator-/blob/main/Reference%20Images/dataneeded.png)

3) Resave the file after exporting from Fathom to remove any encoding issues with the .csv.

4) Upon running the program view first popup:

![image](https://github.com/zdiam/Fathom-Additional-System-Locator-/blob/main/Reference%20Images/gui_window1.png)

5) Upload the file locations of the resaved .csv export (it is beneficial to place this in the same folder as the Python script)

6) Hit the 'Input GPM and Maximum Velocity' Button to continue.

7) Another popup will replace the original:

![](https://github.com/zdiam/Fathom-Additional-System-Locator-/blob/main/Reference%20Images/gui_window2.png)

8) Input the Additional GPM load that the addition to the system will require. Input the maximum allowable fluid velocty required for the location of the additional GPM load.

9) Hit 'Run' button.

10) The output file (.csv) will automatically save in the same file location as the build. File will be saved as *filename of csv*.*#gpm*



   
  

