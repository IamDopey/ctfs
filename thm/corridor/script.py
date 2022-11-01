import hashlib
import requests
  
url = "http://10.10.7.131/"

for i in range(2):
	result = hashlib.md5(str(i).encode())
	hexd = result.hexdigest()
	final_url = url + hexd
	x = requests.get(final_url)
	if b'empty_room.jpg' not in x.content:
		print(hexd)