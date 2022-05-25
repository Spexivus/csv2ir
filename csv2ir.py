#!/usr/bin/python3
import argparse
import os
import sys
import csv

# Ref: http://www.hifi-remote.com/johnsfine/DecodeIR.html
# IRDB referances over 80 IR-protocols
# some of these mapping are if'y due to inconsistent naming
IR_PROTO_REMAP = {
    "Sony12" : "SIRC",
    "Sony15" : "SIRC15",
    "Sony20" : "SIRC20",
    "Tivo unit=0" : "NECext",   #hack
    "NECx1" : "NECext",
    "NECx2" : "NECext",
    "NEC-f16" : "NECext",
    "NEC2-f16" : "NECext",
    "RC5-7F" : "RC5X"
}

# supported by Fipper
# see lib/infrared/encoder_decoder/*/*spec.c
SUPPORTED_IR = [
    "NEC", "NECext", "NEC42", "NEC42ext",
    "RC5", "RC5X", "RC6",
    "Samsung32",
    "SIRC", "SIRC15", "SIRC20",
]

def convert(csv_in, ir_out):
    with open(csv_in, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)        # skip header

        # check ir_protocol
        ir_protocol = next(csv_reader)[1]

        if ir_protocol in IR_PROTO_REMAP:
            ir_protocol = IR_PROTO_REMAP[ir_protocol]

        if ir_protocol not in SUPPORTED_IR:
            print("file {} used IR Protocal {}: Not Supported, Skipped".format(
                csv_in, ir_protocol))
            return

        csv_file.seek(0)
        next(csv_reader)        # skip header

        with open(ir_out, "w") as ir_file:
            ir_file.write("Filetype: IR signals file\n")
            ir_file.write("Version: 1\n")
            for row in csv_reader:
                if not row[0]:
                    continue

                ir_file.write("#\n")
                function_name = row[0].replace(" ", "_")

                ir_file.write(f"name: {function_name}\n")
                ir_file.write("type: parsed\n")
                ir_file.write(f"protocol: {ir_protocol}\n")

                device_id = f"{int(row[2]):02X}"

                subdevice_id = (
                    "00"
                    if (row[3] == "-1")
                    else f"{int(row[3]):02X}"
                )

                command = f"{int(row[4]):02X}"

                ir_file.write(f"address: {device_id} {subdevice_id} 00 00\n")
                ir_file.write(f"command: {command} 00 00 00\n")


def main():
    parser = argparse.ArgumentParser(description="Convert .csv files to .ir files")
    parser.add_argument("input_path", type=str, help="Input file or directory")
    parser.add_argument("output_path", type=str, help="Output file or directory")
    # parser.add_argument("--protocol", type=str, default="NECext", help="IR protocol")
    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        sys.exit(f"Input path not found: {args.input_path}")

    if os.path.isdir(args.input_path):
        for directory in os.walk(args.input_path):
            output_path = os.path.join(
                args.output_path, os.path.relpath(directory[0], args.input_path)
            )
            try:
                os.makedirs(output_path)
            except FileExistsError:
                pass
            for input_file in directory[2]:
                if input_file.endswith(".csv"):
                    output_file = os.path.splitext(input_file)[0] + ".ir"
                    convert(
                        os.path.join(directory[0], input_file),
                        os.path.join(output_path, output_file)
                    )
    else:
        convert(args.input_path, args.output_path)


if __name__ == "__main__":
    main()
