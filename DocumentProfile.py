import json

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
        result = f"====  Document Profile for {self.ein}  ====\n"
        result += f"Taxpayer Name: {self.taxpayername}\n"
        result += f"State: {self.state}\n"
        result += f"ZIP Code: {self.zipcode}\n"
        result += f"Return Type: {self.returntype}\n"
        result += f"Sub Date: {self.subdate}\n"
        result += f"Tax Year: {self.taxyear}\n"
        result += f"Sub Code: {self.subcode}\n"
        result += f"Total Assets: {self.totalassets}\n"
        return result

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)