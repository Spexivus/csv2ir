import argparse
import os
import sys
import csv


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
    parser = argparse.ArgumentParser(description="Convert .csv files to .ir files")
    parser.add_argument("input_path", type=str, help="Input file or directory")
    parser.add_argument("output_path", type=str, help="Output file or directory")
    parser.add_argument("--protocol", type=str, default="NECext", help="IR protocol")
    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        sys.exit(f"Input path not found: {args.input_path}")

    if os.path.isdir(args.input_path):
        if not os.path.exists(args.output_path):
            os.mkdir(args.output_path)
        if not os.path.isdir(args.output_path):
            sys.exit(f"Output path is not a directory: {args.output_path}")
        for input_file in os.listdir(args.input_path):
            if input_file.endswith(".csv"):
                output_file = os.path.splitext(input_file)[0] + ".ir"
                convert(os.path.join(args.input_path, input_file), os.path.join(args.output_path, output_file), args.protocol)
    else:
        convert(args.input_path, args.output_path, args.protocol)


if __name__ == "__main__":
    main()
