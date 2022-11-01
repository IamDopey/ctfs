NMAP:
sudo nmap -p- 10.10.217.102 -Pn

Not shown: 65077 filtered tcp ports (no-response), 452 filtered tcp ports (host-prohibited)
PORT    STATE  SERVICE
21/tcp  closed ftp
22/tcp  closed ssh
80/tcp  closed http
139/tcp closed netbios-ssn
443/tcp closed https
445/tcp closed microsoft-ds

sudo nmap -p 21,22,80,139,443,445 -A -sC -sV  10.10.217.102 -Pn

PORT    STATE SERVICE     VERSION                                                             
21/tcp  open  ftp         vsftpd 3.0.2                                                        
| ftp-anon: Anonymous FTP login allowed (FTP code 230)                                        
|_drwxr-xr-x    2 0        0               6 Jun 09  2021 pub                                 
| ftp-syst:                                                                                   
|   STAT:                                                                                     
| FTP server status:                                                                          
|      Connected to ::ffff:10.9.2.106                                                         
|      Logged in as ftp                                                                       
|      TYPE: ASCII                                                                            
|      No session bandwidth limit                                                             
|      Session timeout in seconds is 300                                                      
|      Control connection is plain text                                                       
|      Data connections will be plain text                                                    
|      At session startup, client count was 1                                                 
|      vsFTPd 3.0.2 - secure, fast, stable                                                    
|_End of status                                                                               
22/tcp  open  ssh         OpenSSH 7.4 (protocol 2.0)                                          
| ssh-hostkey:                                                                                
|   2048 09:23:62:a2:18:62:83:69:04:40:62:32:97:ff:3c:cd (RSA)                                
|   256 33:66:35:36:b0:68:06:32:c1:8a:f6:01:bc:43:38:ce (ECDSA)                               
|_  256 14:98:e3:84:70:55:e6:60:0c:c2:09:77:f8:b7:a6:1c (ED25519)                             
80/tcp  open  http        Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips)                   
| http-methods:                                                                               
|_  Potentially risky methods: TRACE                                                          
|_http-title: Apache HTTP Server Test Page powered by CentOS                                  
|_http-server-header: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips                               
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)                         
443/tcp open  ssl/http    Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips)                   
|_http-title: 400 Bad Request                                                                 
| ssl-cert: Subject: commonName=aratus/organizationName=SomeOrganization/stateOrProvinceName=S
omeState/countryName=--                                                                       
| Not valid before: 2021-11-23T12:28:26                                                       
|_Not valid after:  2022-11-23T12:28:26                                                       
|_ssl-date: TLS randomness does not represent time                                            
|_http-server-header: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips                               
445/tcp open  netbios-ssn Samba smbd 4.10.16 (workgroup: WORKGROUP)

Host script results:
| smb2-time: 
|   date: 2022-04-02T18:38:40
|_  start_date: N/A
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.10.16)
|   Computer name: aratus
|   NetBIOS computer name: ARATUS\x00
|   Domain name: \x00
|   FQDN: aratus
|_  System time: 2022-04-02T20:38:44+02:00
| smb-security-mode: 
|   account_used: guest 
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_clock-skew: mean: -39m57s, deviation: 1h09m12s, median: -1s

Host script results:
|_smb-vuln-ms10-061: false
|_smb-vuln-ms10-054: false
| smb-vuln-regsvc-dos: 
|   VULNERABLE:
|   Service regsvc in Microsoft Windows systems vulnerable to denial of service
|     State: VULNERABLE
|       The service regsvc in Microsoft Windows 2000 systems is vulnerable to denial of service caused by a null deference
|       pointer. This script will crash the service if it is vulnerable. This vulnerability was discovered by Ron Bowes
|       while working on smb-enum-sessions.
|_          


FTP:

drwxr-xr-x    3 0        0              17 Nov 23 09:56 .
drwxr-xr-x    3 0        0              17 Nov 23 09:56 ..
drwxr-xr-x    2 0        0               6 Jun 09  2021 pub

Nothing inside pub directory, tried dir -a to check for hidden files


sudo gobuster dir -u http://10.10.217.102/ -w ~/lists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt

No info!

nikto -h http://10.10.217.102/

+ Server: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ Apache/2.4.6 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ OpenSSL/1.0.2k-fips appears to be outdated (current is at least 1.1.1). OpenSSL 1.0.0o and 0.9.8zc are also current.
+ Allowed HTTP Methods: GET, HEAD, POST, OPTIONS, TRACE 
+ OSVDB-877: HTTP TRACE method is active, suggesting the host is vulnerable to XST
+ OSVDB-3268: /icons/: Directory indexing found.
+ OSVDB-3233: /icons/README: Apache default file found.

Since all the ports besides netbios-ssn or samba does not have a way in or vulnerabilities that we can exploit we will then proceed to analyze the samba shared folders.

