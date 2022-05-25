#!/usr/bin/python3
import argparse
import os
import sys
import csv



SUPPORTED_IR = [
    "NEC", "NECext", "NEC42", "NEC42ext",
    "RC5", "RC5X", "RC6",
    "Samsung32",
    "SIRC", "SIRC15", "SIRC20",
]

def get_protocal(ir_p):
    if ir_p == "Sony12":
        return "SIRC"
    elif ir_p == "Sony15":
        return "SIRC15"
    elif ir_p == "Sony20":
        return "SIRC20"
    elif ir_p == "Tivo unit=0":      # hack
        return "NECext"
    elif ir_p in ["NECx1", "NECx2", "NEC2-f16"]:
        return "NECext"
    elif ir_p == "RC5-7F":
        return "RC5X"

    return(ir_p)

def convert(csv_in, ir_out):
    with open(csv_in, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)        # skip header

        # check ir_protocol
        ir_protocol = next(csv_reader)[1]
        ir_protocol = get_protocal(ir_protocol)
        if ir_protocol not in SUPPORTED_IR:
            print("file {} used IR Protocal {}: Not Supported, Skipped".format(
                csv_in, ir_protocol))
            return

        csv_file.seek(0)
        next(csv_reader)        # skip header

        with open(ir_out, "w") as ir_file:
            ir_file.write(f"Filetype: IR signals file\n")
            ir_file.write(f"Version: 1\n")
            for row in csv_reader:
                if not row[0]:
                    continue

                ir_file.write(f"#\n")
                function_name = row[0].replace(" ", "_")

                ir_file.write(f"name: {function_name}\n")
                ir_file.write(f"type: parsed\n")
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
