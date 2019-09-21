### What's this?

The script allows to simulate mortgage loan basing on a some the most important factors:
* amount of credit         (ex. 300 000)
* bank interest            (ex.2%)
* wibor                    (ex. 2%)
* time to take a loan      (ex. 20 year)
* installment type         (equal/decreasing)

As an output you will be given with two charts:
1. a first tells you what installment would be at each mounth.
   An installement is split on capital and (loan) cost. 
   Of coure, you will have to pay the sum (capital&cost) each mounth.
2. a second sums installment from each mount and at the end you will see the entire cosnt of your loan. 
   This should be the most important asset for you.

The charts shall appear in your internet browser.

### Install required packages
```
pip3 install -r requirements.txt
```

The script was being tested with *Mozilla firefox 68.0.2(64-bit ) for Linux Mint*

### How to use calculator?

```
python3 main.py [args]
```
###### Arguments description
```
'-l',       '--loan',                  "Amount of credit [ex. 300000]"
'-bi',      '--bank_interest',         "Bank interest [ex. 2%]"
'-w'        '--wibor'                  "Warsaw Interbank Offered Rate [ex. 2%]"
'-y'        '--loan_diuration'         "A loan duration [ex. 20 year]"
'-it'       '--installment_type'       "An installement type [equal/decreasing]"

run example:
python3 main.py -l 300000 -bi 2 -w 2 -y 20 -it equal
```
