import os
import csv
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
        protocol = str(input("\nEnter the protocol you would like to use \n Currently supported protocols: NEC, NECext, Samsung32).\n"))

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
                            protocol = row[1]   # Protocol row
                        else :
                            protocol = "NECext"

                        irFile.write(f"name: {functionName}\n")                 # name
                        irFile.write(f"type: parsed\n")                         # type

                        irFile.write(f"protocol: {protocol}\n")

                        deviceID = row[2]  # Device row
                        subdeviceID = row[3] # Subdevice row

                        if subdeviceID == deviceID:
                            subdeviceID = (hex(int(deviceID)))[2:]  # Set equal to deviceID if subdeviceID is same
                        if row[2] != row[3]:
                            deviceID = (hex(int(deviceID)))[2:]     # Device ID to hex
                            subdeviceID = (hex(int(subdeviceID)))[2:]   # Subdevice ID to hex
                            if len(deviceID) == 1:
                                deviceID += "0"
                            if len(subdeviceID) == 1:
                                subdeviceID += "0"

                            irFile.write(f"address: {deviceID} {subdeviceID} 00 00\n")

                        else:
                            deviceID = (hex(int(deviceID)))[2:]
                            if len(deviceID) == 1:
                                deviceID = "0" + deviceID
                            irFile.write(f"address: {deviceID} 00 00 00\n")
                        command = (hex(int(row[4])))[2:]
                        if len(command) == 1:
                            command = "0" + command
                        irFile.write(f"command: {command} 00 00 00\n")

    finish = time.time()
    print(f"\nConverted {counter} files in {finish-start} seconds ({counter/(finish-start)} files per second)")
    print("Auto-quitting in 5 seconds... ")
    time.sleep(5)
    quit()


main()
