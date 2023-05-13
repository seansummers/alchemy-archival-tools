class DocumentProfile:
    def __init__(self, ein, returntype, state, subcode, subdate, taxyear, taxpayername, totalassets, zipcode):
        self.ein = ein
        self.returntype = returntype
        self.state = state
        self.subcode = subcode
        self.subdate = subdate
        self.taxyear = taxyear
        self.taxpayername = taxpayername
        self.totalassets = totalassets
        self.zipcode = zipcode

def __str__(self):
    result = f"==== Document Profile for {self.ein}  ====\r"
    result += f"Return Type: {self.returntype}\r"
    result += f"State: {self.state}\r"
    result += f"Sub Code: {self.subcode}\r"
    result += f"Sub Date: {self.subdate}\r"
    result += f"Tax Year: {self.taxyear}\r"
    result += f"Taxpayer Name: {self.taxpayername}\r"
    result += f"Total Assets: {self.totalassets}\r"
    result += f"ZIP Code: {self.zipcode}\r"
    return result
