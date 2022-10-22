# Solution

We need to find a password for the user that created a backup at the time of the breach.
filter tcp.len>0 then search for "Pakcet bytes" the string "pass"
We found: mysql -u backup -p backup123
flag{backup123}

