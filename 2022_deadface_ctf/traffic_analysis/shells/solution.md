# Solution

To start we first filter for tcp.len>0 to remove all ack, SYN and RST requests.
THen we search for "Packet Bytes" and "string" = info.php

We notice that the string "info.php" is in a data that appears to be the result of an ls command, it means that the attacker probably already had access to the system.
We go back a few request and we see "b374k shell : connected" 

flag{b374k}
