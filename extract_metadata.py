import DocumentProfile

# TODO: Download more disks and figure out the folder structure so users can specify the location of the disk and not have to hunt down the specific file
filename = r"C:\Users\vince\Dropbox\00 Grad School\05 Summer 2023\Test disk\1998 Jul - Dec; Private Foundation Returns for ALABAMA; pfal000s001\PFAL000S\DATA000\00001.PRO"
START_CODE = '0023000A'
END_CODES = ['000701240006', '000701250003', '000701260002', '000701270008', '000701280007', '000701290013', '0007012A0007', '0007012B0006']
    # Note to self: Each of these start with [00 07 01]
    # followed by three more bytes. Find just that?
END_ALL_CODE = '000305190000'


# Convert these codes into bytes
start_code = bytes.fromhex(START_CODE)
end_codes = [bytes.fromhex(code) for code in END_CODES]
end_all_code = bytes.fromhex(END_ALL_CODE)

def main():
  with open(filename, 'rb') as f:
      data = f.read()

  # Find each record's position in the binary file
  all_start_offsets = []
  pos = data.find(start_code) # Find the first instance of the start code
  while pos != -1: # Loop until it can't find any more
    all_start_offsets.append(pos)
    pos = data.find(start_code, pos + 1) # Look for another one!

  for offset in all_start_offsets:
    start_pos = offset
    for code in end_codes:
        end_pos = data.find(code, offset)
        if end_pos != -1:
            result = data[start_pos:end_pos].decode('unicode_escape')
            print(result)
            start_pos = start_pos + len(result) + len(code)
        else:
            break

# TODO: Turn stuff into methods + a main()

# TODO: Idea for a better search method:
#  Get offset of start_code
#  Get offset of end_all_code
#  find() the next instance of [00 07 01 * * *]
#  Use the DocumentProfile class.
#  If said instance is after end_all_code, the record is complete
#  and it's time to search for the next instance of start_code,
#  using the offset of end_all_code as a starting point.

if __name__ == "__main__":
    main()