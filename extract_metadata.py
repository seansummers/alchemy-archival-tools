import re
import DocumentProfile
from secrets import filename

# TODO: Download more disks and figure out the folder structure so users can specify the location of the disk and not have to hunt down the specific file
START_CODE = '0023000A'
END_CODES = ['000701240006', '000701250003', '000701260002', '000701270008', '000701280007', '000701290013', '0007012A0007', '0007012B0006'] # TODO: Delete this?
    # Note to self: Each of these start with [00 07 01]
    # followed by three more bytes. Find just that?
END_ALL_CODE = '000305' # These codes start with 00 03 05 and are followed by three more bytes
END_ALL_CODE_2 = '000206' # Sometimes they end with this code instead. I wonder why...

# Convert these codes into bytes
start_code = bytes.fromhex(START_CODE)
end_codes = [bytes.fromhex(code) for code in END_CODES] # TODO: Delete this?
end_code = bytes.fromhex('000701')
end_all_code = bytes.fromhex(END_ALL_CODE)
end_all_code_2 = bytes.fromhex(END_ALL_CODE_2)

def main():
    with open(filename, 'rb') as f:
        data = f.read() # This "data" variable is where the entire file's contents is going to be stored

    all_start_offsets = []
    pos = data.find(start_code) # Find the first instance of the start code
    while pos != -1: # Loop until it can't find any more
      all_start_offsets.append(pos)
      pos = data.find(start_code, pos + 1) # Look for another one!
    
    # Now all_star_offsets contains the locations of each record in the file.

    index = 0 # Keep track of how many records we've looked at
    records = [] # This will contain instances of DocumentProfile
    for start_offset in all_start_offsets: # Loop through each record
        result = []
        # TODO: Add the first field
        current_offset = start_offset + len(start_code) # Keep track of where we are, starting at the start of the current record
        
        # The EIN is the first field in each record. Get it and add it to the result
        ein_end_offset = data.find(end_code, current_offset + 1)
        ein = get_text(data, current_offset, ein_end_offset)
        result.append(ein)

        while (True): # TODO: lol it's a while true. Is there a better way to structure this?
            current_offset = data.find(end_code, current_offset) + 6
            next_offset = data.find(end_code, current_offset + 1) # This is where we'll be stopping. The +1 is just to get it to find the next one
            
            # Check to see if the next_offset is in the middle of the next record
            if (next_offset > all_start_offsets[index + 1]):
                next_offset = data.find(00, current_offset + 1) # Find the next 0x00, which is the end of the record.
                line = get_text(data, current_offset, next_offset) # Get the final line!
                result.append(line)
                current_offset = data.find(start_code, current_offset + 1) # Set the current offset to the start of the next record. This will cause the while loop to end!
                break # skip the rest of the code here and continue to the next record
            
            line = get_text(data, current_offset, next_offset) # get the line
            result.append(line)
        
        temp = DocumentProfile(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])
        print(temp)
        records.append(temp)
        
        index = index + 1


def get_text(data, start_offset, end_offset):
    return data[start_offset:end_offset].decode('unicode_escape')

# TODO: Idea for a better search method:
#  Get offset of start_code
#  Get offset of end_all_code
#  find() the next instance of [00 07 01 * * *]
#  Use the DocumentProfile class.
#  If said instance is after end_all_code, the record is complete
#  and it's time to search for the next instance of start_code,
#  using the offset of end_all_code as a starting point.




# The following is my first attempt:
# all_start_offsets = []
# pos = data.find(start_code) # Find the first instance of the start code
# while pos != -1: # Loop until it can't find any more
#   all_start_offsets.append(pos)
#   pos = data.find(start_code, pos + 1) # Look for another one!
# 
# for offset in all_start_offsets:
#   start_pos = offset
#   for code in end_codes:
#       end_pos = data.find(code, offset)
#       if end_pos != -1:
#           result = data[start_pos:end_pos].decode('unicode_escape')
#           print(result)
#           start_pos = start_pos + len(result) + len(code)
#       else:
#           break

# TODO: Turn stuff into methods + a main()

if __name__ == "__main__":
    main() # Run the dang thing!