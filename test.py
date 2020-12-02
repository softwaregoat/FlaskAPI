import requests

url = "http://18.216.133.108:8080/api/uploader?api_key=12345"

payload={}
files=[
  ('files[]', open('C:/Users/Software/Downloads/filename1.txt', 'rb')),
  ('files[]', open('C:/Users/Software/Downloads/sample_dictionary_file.txt', 'rb'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)