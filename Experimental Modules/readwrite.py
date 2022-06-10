#import ast
import json
import io
import os

#https://stackoverflow.com/questions/32991069/python-checking-for-json-files-and-creating-one-if-needed
#https://www.youtube.com/watch?v=9N6a-VLBa2I (9 Minutes)

def where_json(file_name):
    return os.path.exists(file_name)

if where_json('data.json'):
    print("File Exists")
    pass

else:
    new_data = {
        'meme_collected': 0,
        'deaths': 5,
        'is_perfect_save': False
    }
    with open('data.json', 'w') as outfile:
        print("Does not exist, creating json file")
        json.dump(new_data, outfile)


with open('data.json') as its_raw:
    data = json.load(its_raw)

print(data)

for lucario in data['lucario']:
    del lucario['is_perfect_save']

print(data)

with open('WIIdata.json', 'w') as fresh_data:
    json.dump(data, fresh_data, indent=2)

#data = {
#'meme_collected': input('How many memes collected?: '),
#'deahts': input('How many times have you died?: ')
#}
#with open('data.json', 'w') as outfile:
#    json.dump(data, outfile)

#for Header in its_raw['header']:
    #del Header['Wii']
    #print(Header['U'])

#new_string = json.dumps(PyData, indent=2, sort_keys=True)

#print(new_string)

#print(type(PyData['Header']))
#print(PyData)

input("Press Enter to Continue")
