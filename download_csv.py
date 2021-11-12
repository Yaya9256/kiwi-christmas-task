import os
import requests

source = "https://raw.githubusercontent.com/kiwicom/python-weekend-xmas-task/5d608fcbc259f4c0520cbc3b5598279f965cb5f1/example/example0.csv"
name_file = source.rsplit("/")[-1]

if not os.path.exists(name_file):
    print(f"File {name_file} is not downloaded...")
    response = requests.get(source)
    with open(name_file, "wb") as out:
        out.write(response.content)
    print(f"File {name_file} downloaded successfully.")
else:
    print(f"File copy {name_file} already downloaded.")
