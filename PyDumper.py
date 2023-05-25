"""
Github : https://github.com/Namx45
"""



from os import path as ospath
log_file_path = ""
__name__ = "__pyhexdumper__"

class file:

    full_path = ""
    dir_path = ""
    name = ""
    size = 0

    hex_dump = []
    global log_file_path

    # get file/path from user & sets file vars
    def __init__(self):
        user_input = input("Enter file name (Or path; path can be in quotes)\n")
        try:
            if ("\\" not in user_input):
                 self.full_path = os.getcwd() + user_input
            elif ("\"" in user_input):
                self.full_path = user_input.split("\"")[1]
                self.full_path = user_input.split("/")[1]
                self.dir_path = ospath.dirname(self.full_path)
                self.name = self.full_path.split(self.dir_path)[1]
            elif("\'" in user_input):
                self.full_path = user_input.split("\'")[1]
                self.full_path = user_input.split("/")[1]
                self.dir_path = ospath.dirname(self.full_path)
                self.name = self.full_path.split(self.dir_path)[1]
            else:
                self.full_path = user_input
                self.dir_path = ospath.dirname(self.full_path)
                self.name = self.full_path.split(self.dir_path)[1]
            self.size = ospath.getsize(self.full_path) # size in bytes
        except Exception as ex:
            msg = """Something went wrong while 
Retriving the file, try again..."""
            self.full_path = None
            print(ex)
            print(msg)

    # creates a hex dump as a list (without '0x' symbol)    
    def dump_hex(self):
        try:
            with open(self.full_path, "rb") as file:
                for byte in file.read(self.size):
                    self.hex_dump.append(hex(byte)[2:])
            return self.hex_dump
        except Exception as ex:
            print(ex)
            print("""Error while reading file in binary mode
Try to check file encoding / file types supported & rerun script.""")
            
    # prints hex dump (to file or shell)
    def print_dump(self, mode):
        if (self.hex_dump == None): 
            print("Hex dump: N/A")
            return
        counter_byte = 0
        counter_offset = 0
        offset = ""
        first_offset = "     00 01 02 03 04 05 06 07" # 08 09 0A 0B 0C 0D 0E 0F")
        self.log_file_path = ospath.join(self.dir_path, "log.txt") ##$##$##
        try: 
            if (mode == "shell"):
                print(first_offset)
            elif (mode == "log"):
                with open(self.log_file_path, "a") as log_file:
                    log_file.write(f"File path + name: {self.full_path}\n")
                    log_file.write(first_offset)
        except Exception as ex:
            print(ex)
            print("""Error writing log file
Check permission in imported file/folder""")
            return

        # print in hex dump format
        for byte in self.hex_dump:
            if(len(byte) < 2):
                byte = f"0{byte}"
            if counter_byte < 7: #< 15:
                offset = offset + byte + " "
                counter_byte = counter_byte + 1
            else:
                line = f"0x{counter_offset}: {offset}{byte}"
                if (mode == "shell"):
                    print(line)
                elif (mode == "log"):
                    with open (self.log_file_path, "a") as log_file:
                        log_file.write(f"\n{line}\n")
                counter_byte = 0
                counter_offset = counter_offset + 1
                offset = ""  

# change things here to add files / control where to send hex dump data 
def main():
    mode = "log" # print modes: shell, log
    # TODO: add json+xml in print_dump modes
    file1 = file()
    while file1.full_path is None:
        file1 = file()
    file1_Hexdump = file1.dump_hex()
    file1.print_dump(mode) 
    print(f"Log file is saved under this PATH: {log_file_path}")
main()
