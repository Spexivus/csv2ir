import os
import csv
from re import sub
import time


def main():
    mainPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\csv2ir"
    csvPath = mainPath + "\csv"
    irPath = mainPath + "\ir"

    if os.path.exists(mainPath) == False:

        os.mkdir(mainPath)
        os.mkdir(csvPath)
        os.mkdir(irPath)
        print(f"Created main directory ({mainPath})\n")

    if input(f"Place .csv files in the ({csvPath}) directory. Should I open it for you? (y/n). \n") == "y":
        os.startfile(csvPath)
    input("\nPress enter when you are finished placing files.")

    if input("\nWould you like to set a custom protocol? (y/n)\n") == "y":
        customProtocol = True
        protocol = str(input("\nEnter the protocol you would like to use \nCurrently supported protocols: NEC, NECext, Samsung32).\n"))

    os.chdir(csvPath)
    csvfiles = os.listdir()  # list of csv files

    if len(csvfiles) == 0:
        print("\nNo csv files found. Exiting...")
        time.sleep(2)
        exit()

    counter = 0
    print("\nConverting files... ")
    start = time.time()

    for file in csvfiles:
        if file.endswith(".csv"):
            os.chdir(csvPath)
            with open(file, newline='') as csvFile:
                csv_reader = csv.reader(csvFile, delimiter=',')
                next(csvFile)
                filename = file.replace(".csv", ".ir")
                os.chdir(irPath)
                counter += 1
                with open(filename, "w") as irFile:
                    irFile.write(f"Filetype: IR signals file\n")
                    irFile.write(f"Version: 1\n")
                    for row in csv_reader:
                        irFile.write(f"#\n")
                        functionName = row[0].replace(" ", "_")

                        if customProtocol == False:
                            protocol = "NECext"

                        irFile.write(f"name: {functionName}\n")                 # name
                        irFile.write(f"type: parsed\n")                         # type

                        irFile.write(f"protocol: {protocol}\n")

                        deviceID = row[2]  # Device row
                        deviceID = (hex(int(deviceID)))[2:].replace('x', '0')

                        subdeviceID = row[3] # Subdevice row
                        subdeviceID = (hex(int(subdeviceID)))[2:].replace('x', '0')

                        command = (hex(int(row[4])))[2:]  # Command row (in hex)

                        if subdeviceID == deviceID:
                            subdeviceID = "00"
                        elif row[3] == "-1":    # Check value before conversion
                            subdeviceID = "00"

                        if len(deviceID) == 1:
                            deviceID = "0" + deviceID
                        if len(subdeviceID) == 1:
                            subdeviceID = "0" + deviceID

                        irFile.write(f"address: {deviceID} {subdeviceID} 00 00\n")

                        if len(command) == 1:
                            command = "0" + command
                        irFile.write(f"command: {command} 00 00 00\n")

    finish = time.time()
    print(f"\nConverted {counter} files in {finish-start} seconds ({counter/(finish-start)} files per second)")
    print("Auto-quitting in 5 seconds... ")
    time.sleep(5)
    quit()


main()
