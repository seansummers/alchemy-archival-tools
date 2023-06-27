from DocumentProfile import DocumentProfile
from secrets import list_of_files
from pathlib import Path

def main():
    for filename in list_of_files:
        current_title = get_cdrom_name(filename)

        with open(filename, 'rb') as f:
            data = f.read() # This "data" variable is where the entire file's contents is going to be stored

        records = extract(data)
        save_json_file(records, current_title)

########################################################################

def extract(data):
    start_code = convert_to_bytes('0023000A') # This code is right before the data starts
    # Note to self: Each of the fields are separated by codes that start with [00 07 01] followed by three more bytes.

    # Find the location of each record in the file
    all_start_offsets = []
    pos = data.find(start_code) # Find the first instance of the start code
    while pos != -1: # Loop until it can't find any more
      all_start_offsets.append(pos)
      pos = data.find(start_code, pos + 1) # Look for another one!
    
    # Extract each record present
    index = 0 # Keep track of how many records we've looked at
    records = [] # This will contain instances of DocumentProfile
    for start_offset in all_start_offsets: # Loop through each record
        result = []
        current_offset = start_offset + len(start_code) # Keep track of where we are, starting at the start of the current record
        
        # The EIN is the first field in each record. Get it and add it to the result
        ein_end_offset = data.find(00, current_offset + 1)
        ein = get_text(data, current_offset, ein_end_offset)
        result.append(ein)

        if index >= len(all_start_offsets):
            break # Skip the rest of this if there aren't any more records to read

        for x in range(8): # Each record has eight fields
            current_offset = data.find(00, current_offset) + 6
            next_offset = data.find(00, current_offset + 1) # This is where we'll be stopping. The +1 is just to get it to find the next one
            line = get_text(data, current_offset, next_offset) # Get the text!
            result.append(line)
        
        current_offset = data.find(start_code, current_offset + 1) # Set the current offset to the start of the next record.

        temp = DocumentProfile(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])
        records.append(temp)
        index = index + 1
    return records


# Helper methods!
def get_cdrom_name(filename):
    return Path(filename).resolve().parents[2].name # This takes the whole filepath and returns just the name of the folder.

def get_text(data, start_offset, end_offset):
    return data[start_offset:end_offset].decode('unicode_escape')

def convert_to_bytes(input):
    return bytes.fromhex(input) # Converts a string that contains a hex number into that number. Simple but this looks cleaner.

def save_json_file(records, directory_name):
    result = ""
    with open(f"metadata for {directory_name}.json", "a") as write_file:
        for record in records:
            result = record.toJSON() + "\r\n"
            write_file.write(result)
            print(result) # Debug

# Now that everything's defined, run the dang thing!
if __name__ == "__main__":
    main()

# TODO: Generally clean up the code.

# TODO: Download more disks and figure out the folder structure so users can specify
#       the location of the disk and not have to hunt down the specific file
