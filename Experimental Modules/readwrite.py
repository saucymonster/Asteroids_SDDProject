import ast
import json
import io
import os

#https://stackoverflow.com/questions/32991069/python-checking-for-json-files-and-creating-one-if-needed

def where_json(file_name):
    return os.path.exists(file_name)

if where_json('data.json'):
    print("File Exists")
    pass

else:
    data = {
        'user': input('User input: '),
        'pass': input('Pass input: ')
    }
    with open('data.json', 'w') as outfile:
        print("Does not exist, creating json file")
        json.dump(data, outfile)


with open('data.json') as its_raw:
    data = json.load(its_raw)

for Header in its_raw['header']:
    #del Header['Wii']
    print(Header['U'])

#new_string = json.dumps(PyData, indent=2, sort_keys=True)

#print(new_string)

#print(type(PyData['Header']))
#print(PyData)

