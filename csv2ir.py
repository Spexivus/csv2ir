import os
import csv
from re import sub
import time


def convert(csv_in, ir_out, protocol="NECext"):
    with open(csv_in, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_file)
        with open(ir_out, "w") as ir_file:
            ir_file.write(f"Filetype: IR signals file\n")
            ir_file.write(f"Version: 1\n")
            for row in csv_reader:
                ir_file.write(f"#\n")
                function_name = row[0].replace(" ", "_")

                ir_file.write(f"name: {function_name}\n")
                ir_file.write(f"type: parsed\n")
                ir_file.write(f"protocol: {protocol}\n")

                device_id = (hex(int(row[2])))[2:].replace('x', '0').upper()
                if len(device_id) == 1:
                    device_id = "0" + device_id

                subdevice_id = "00" if (row[3] == "-1") else (hex(int(row[3])))[2:].replace('x', '0').upper()
                if len(subdevice_id) == 1:
                    subdevice_id = "0" + subdevice_id

                command = (hex(int(row[4])))[2:].upper()
                if len(command) == 1:
                    command = "0" + command

                ir_file.write(f"address: {device_id} {subdevice_id} 00 00\n")
                ir_file.write(f"command: {command} 00 00 00\n")


def main():
    mainPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\csv2ir"
    csvPath = mainPath + "\csv"
    irPath = mainPath + "\ir"
    customProtocol = False

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
    else:
        protocol = "NECext"

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
            convert(os.path.join(csvPath, file), os.path.join(irPath, file.replace(".csv", ".ir")), protocol)

    finish = time.time()-start
    print(f"\nConverted {counter} files in {finish} seconds ({counter/(finish)} files per second)")
    print("Auto-quitting in 5 seconds... ")
    time.sleep(5)
    quit()


main()
