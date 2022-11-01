import hashlib
  
# initializing string
str2hash = "a"
hex = ""
while(hex != "001"):
	str2hash += "a"
	result = hashlib.md5(str2hash.encode())
	hex = result.hexdigest()[-3:]

print("this is the out" + str2hash)

