import re
import DocumentProfile
from secrets import filename

# TODO: Download more disks and figure out the folder structure so users can specify the location of the disk and not have to hunt down the specific file
START_CODE = '0023000A'
END_CODES = ['000701240006', '000701250003', '000701260002', '000701270008', '000701280007', '000701290013', '0007012A0007', '0007012B0006']
    # Note to self: Each of these start with [00 07 01]
    # followed by three more bytes. Find just that?
END_ALL_CODE = '000305190000'


# Convert these codes into bytes
start_code = bytes.fromhex(START_CODE)
end_codes = [bytes.fromhex(code) for code in END_CODES] # TODO: Delete this?
end_code = bytes.fromhex('000701')
end_all_code = bytes.fromhex(END_ALL_CODE)

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
    for offset in all_start_offsets: # Loop through each record
        result = []
        current_offset = offset # Keep track of where we are
        while current_offset < all_start_offsets[index + 1]: # Don't bleed over into the next record!
            current_offset = data.find(end_code, current_offset) + 6
            next_offset = data.find(end_code, current_offset + 1) # This is where we'll be stopping. The +1 is just to get it to find the next one
            # TODO: What if it's the end_all_code that's next? Should probably check for that too
            line = data[current_offset:next_offset].decode('unicode_escape')
            result.append(line)
        print(result)


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