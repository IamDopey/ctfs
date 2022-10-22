# Solution

To get the user that DEADFACE tried to add we use the same method for previous challenges

filter: tcp.len>0
Find Packet: "packet bytes", "string"="INSERT".
We got:
```
 mysql -u backup -pbackup123 -D esu -e "INSERT INTO users (username, first, last, email, street, city, state_id, zip, gender, dob) VALUES ('areed2022', 'Alexandra', 'Reed', 'fake@email.com', '830 Iowa Place', 'Reese', 23, '48757', 'f', '1999-08-19');"
```
flag{areed2002}
