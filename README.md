# Domain Checker script
This is a small script I made to check for domain existance/registration.
The script was inspired by namecheap.com's "Beast mode" search.


### Installation / dependencies:
Download/copy/clone  the main.py script and i nstall all the dependencies with
```
pip install -r requirements.txt
# or
pip3 install -r requirements.txt

```
### Usage:

You can run the script with

```
python3 ./main.py
```
or

```
py ./main.py
```
if you are on Windows.

### What the script will do

The script will ask you for a domain name you like, without TLD. When you give a name, it will try to combine it with 
the TLDS it finds in the `tlds.txt` file. 

If you want to edit the file or add new tlds, remember they must be separated
by newlines. The default file is given with all the existing TLDS at August 2021.


With the list of possible domain names, the script will then query chosen DNSs for their `NS` record for that domain, the
idea is that registered domains should have at least the `NS` record. If it doesn't find it or times out, it will also try the `A` record.

The script will output a timestamped (eu format) CSV file with data for all possible domains in the working directory.