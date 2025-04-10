def dump_start_of_file(file_path, size=512):
    with open(file_path, "rb") as f:
        data = f.read(size)
        hex_dump = ' '.join(f'{b:02X}' for b in data)
        print(hex_dump)

if __name__ == "__main__":
    dump_start_of_file("SCRIPT.THFS", 512)
