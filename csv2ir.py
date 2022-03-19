from dataclasses import replace
import os
import csv

def main():
    mainPath = os.getcwd() + "\csv2ir"
    csvPath = mainPath + "\csv"
    irPath = mainPath + "\ir"

    if os.path.exists(mainPath) == False:

        os.mkdir(mainPath)
        os.mkdir(csvPath)
        os.mkdir(irPath)

    input("Place .csv files in the csv directory and press enter to continue...")


    os.chdir(csvPath)
    csvfiles = os.listdir() #list of csv files

    for file in csvfiles:
        if file.endswith(".csv"):
            os.chdir(csvPath)
            with open(file, newline='') as csvFile:
                csv_reader = csv.reader(csvFile, delimiter=',')
                next(csvFile)
                filename = file.replace(".csv", ".ir")
                os.chdir(irPath)
                with open(filename, "w") as irFile:
                    irFile.write(f"Filetype: IR signals file\n")
                    irFile.write(f"Version: 1\n")
                    for row in csv_reader:
                        irFile.write(f"#\n")
                        functionName = row[0].replace(" ","_")
                        irFile.write(f"name: {functionName}\n")
                        irFile.write(f"type: parsed\n")
                        if row[1] == "NECx1" or row[1] == "NECx2" or row[1] == "NEC1" or row[1] == "NEC2":
                            irFile.write(f"protocol: NEC\n")
                        #elif row[1] == "protocol_here":
                        #    irFile.write(f"protocol: protocol_here\n")
                        else:
                            irFile.write(f"protocol: {row[1]}\n")
                        if row[2] != row[3]:
                            row1 = (hex(int(row[2])))[2:]
                            row2 = (hex(int(row[3])))[2:]
                            if len(row1) == 1:
                                row1 += "0"
                            if len(row2) == 1:
                                row2 += "0"
                            irFile.write(f"address: {row1} {row1} 00 00\n")
                        else:
                            row1 = (hex(int(row[2])))[2:]
                            if len(row1) == 1:
                                row1 = "0" + row1
                            irFile.write(f"address: {row1} 00 00 00\n")
                        cRow = (hex(int(row[4])))[2:]
                        if len(cRow) == 1:
                            cRow = "0" + cRow
                        irFile.write(f"command: {cRow} 00 00 00\n")

main()