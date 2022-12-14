# Fathom-Additional-System-Locator
Fathom additional system locator to determine which locations on a campus system chilled water hydraulic model will allow for connections of additional buildings based on new GPM load and allowed maximum velocity 


Required export outputs : Pipe #, Pipe Nominal Size,Vol. Flow Rate (gal/min), Velocity (feet/sec) as a .csv file. Resave the file after exporting from Fathom to remove any encoding issues with the .csv
The script will locate these from an AFT Fathom export (AFT Fathom 11)

Final output file will be placed into the same folder as .csv upload location

File will be saved as *filename*.*#gpm*
