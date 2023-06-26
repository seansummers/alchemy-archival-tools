from DocumentProfile import DocumentProfile
from secrets import filename

def main():
    start_code = convert_to_bytes('0023000A') # This code is right before the data starts
    # Note to self: Each of the fields are separated by codes that start with [00 07 01] followed by three more bytes.

    with open(filename, 'rb') as f:
        data = f.read() # This "data" variable is where the entire file's contents is going to be stored

    current_cdrom_title = "TODO" # Figure out how to get this!

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

    save_metadata(records, current_cdrom_title) # Save to a file

# Helper methods!
def get_text(data, start_offset, end_offset):
    return data[start_offset:end_offset].decode('unicode_escape')

def convert_to_bytes(input):
    return bytes.fromhex(input) # Converts a string that contains a hex number into that number. Simple but this looks cleaner.

def save_metadata(records, directory_name):
    result = ""
    # Save as JSON
    with open(f"metadata_{directory_name}.json", "a") as write_file:
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

# TODO: Alter save_metadata to use the directory name when saving the .JSON file
# Ideas: Maybe use a text file that's full of paths for it to rip through, and somehow gleam it from that?
# How many of these CD-ROMs can I download onto my computer at once, though?
# Does that matter? A user (or me) might want to do small batches.
# File structure is entirely in OneDrive...
# C:\Users\olivia\Indiana University\O365-[Sec] IN-ULIB-BornDigital - Mss005\Mss005_[four-digit index number]\[THE DIRECTORY NAME WE WANT]\PFAL000S\DATA000\00001.PRO
