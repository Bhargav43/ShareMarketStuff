# [ShareMarketStuff](https://github.com/Bhargav43/ShareMarketStuff)
## 1. [SharePriceNotifier](https://github.com/Bhargav43/ShareMarketStuff/tree/master/SharePriceNotifier%201.2.0)
### Purpose :bulb:
_Share Market_: is where buying and selling of share happens. Share represents a unit of ownership of the company from where you bought it.

_BSE & NSE_: In India, there are two major stock exchanges – NSE or National Stock Exchange & BSE or Bombay Stock Exchange. BSE is the oldest stock exchange in Asia while NSE is the largest in the country.

_Useful Site_: [Money Control](https://www.moneycontrol.com/) is one of the best site for live price updates, and other essential details useful for trading shares.

[`SharePriceNotifier`](https://github.com/Bhargav43/ShareMarketStuff/tree/master/SharePriceNotifier%201.2.0) is a simple application developed for automated-notifications on the selected share when its price reaches expected margin.

### Base System's Configurations :wrench:
**Sno.** | **Name** | **Version/Config.**
-------: | :------: | :------------------
1 | Operating System | Windows 10 x64 bit
2 | Python | Version 3.7.0 x64 bit
3 | PyInstaller | Version 3.6
4 | IDE | Pyzo 4.10.2 x64 bit

_Recommendation: Try using [`executable`](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/SharePriceNotifier.exe) directly as it doesn't require Python and other dependencies to be present in your Windows PC. Executable is mostly made stand-alone._ 

### Requirements :heavy_exclamation_mark:
1. Reliable internet connection as slow connections may cause delay in live data fetch.
1. Select share by the starting letter when prompted as the total number of companies in the market are huge to fetch and display.

By 2-Jun-2020,
* No. of Companies in Market = 8641
* Expected Fetches Per Second = 5 Requests

### Imported Modules :package:
Sn | **Module** | **Type** | **Version**
-: | :--------: | :------- | :----------
1 | os | *Built-in* | NA
2 | time | *Built-in* | NA
3 | json | *Built-in* | NA
4 | win10toast | *PyPI Installed* | 0.9
5 | requests | *PyPI Installed* | 2.23.0
6 | beautifulsoup4 | *PyPI Installed* | 4.9.1

### [Scripts](https://github.com/Bhargav43/ShareMarketStuff/tree/master/SharePriceNotifier%201.2.0/Scripts) :page_facing_up:
#### 1/5 [SharePriceNotifier.py](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/Scripts/SharePriceNotifier.py)
The main function of the whole app which consolidates between all the other scripts.
```python
import DataScrapper as ds
import User_Inputs as ui
import Operations as op
import SaveLogs as sl

def main():
    Shares = ds.ListOfShares()
    Selected = ui.UserInput(Shares)
    payload = Shares[Selected]
    payload.update(name=Selected)
    filterType, vals = ui.Filtering(payload)
    try:
        op.NotificationLogger(payload, filterType, vals)
    except KeyboardInterrupt:
        print('\n--Interrupted--')

    log = sl.save_logs(op.collection)
    print(f'\nYour Notification\'s Log is Saved At:\n{log}') if log else print('\n!!!No Logs to Save!!!')

    input('\nPress Any Key to Exit.')

if __name__=='__main__':
    main()
```
#### 2/5 [User_Inputs.py](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/Scripts/User_Inputs.py)
As the name suggests, this module is for interacting with the user for inputs.
```python
import time
import DataScrapper as ds

def Selector(lst, let='all'):
    shares = [l for l in lst if l.upper().startswith(let)] if let!='all' else [l for l in lst]
    lister = lambda: (print(f'\nList of \'{let.upper()}\' Shares:\nSno.\tName'), [print(f'{i+1}\t{shares[i]}') for i in range(len(shares))])

    counter = 0
    lister()
    while True:
        counter+=1
        if counter == 3 and let != 'all':
            lister()
            counter = 0
        try:
            inp = int(input(f'\nYour Share [1,{len(shares)}]:\t'))-1
            if not inp in [i for i in range(len(shares))]:
                print('Out of Bounds.', end=' ')
                raise
            break
        except Exception:
            print('Invalid Entry. Retry')
            time.sleep(2)

    return shares[inp]

def UserInput(lst):
    print(f'There are a total of {len(lst)} shares. To make the selection simple, use the followning option:\n1. Specific Alphabet\'s Shares.\n2. Else, All Shares.')
    while True:
        try:
            op = int(input('\nYour Option? [1, 2]\t'))
            if not op in (1, 2):
                print('Option Should Be 1 or 2.', end=' ')
                raise
            break
        except Exception:
            print('Invalid Entry. Retry.')

    if op==1:
        print('Great! Now Enter The Letter (Case-Insensitive) You Want to Shortlist.', end=' ')
        while True:
            try:
                let = input('Your Letter? [A-Z]\t')
                let = let.upper() if len(let)==1 and let.upper() in [chr(i) for i in range(65, 91)] else 'Invalid'
                print(f'Your Letter is {let}')
                if let == 'Invalid':
                    raise
                else:
                    break
            except Exception:
                print('Invalid Entry. Retry.')


        share = Selector(lst, let)

    else:
        print('That\'s Old-School. No Probs. But You Gotta Wait While It Prints...', end=' ')
        time.sleep(2)
        share = Selector(lst)

    print(f'\nGreat! You\'ve Selected {share}\n' )

    return share


def Filtering(share):

    while True:
        try:
            current = ds.getvalues(share['key'])
            break
        except Exception:
            print('Could Be Network Error. Retrying.')
            time.sleep(5)
    while True:
        try:
            ty = int(input(f'\n{share["name"]}\'s present BSE, NSE values are {current}\nYou can Cross-Check from {share["url"]}\n\nPlease Select Type of Alert (Applies for both BSE and NSE)\n1.Higher Than\n2.Less Than\n3.Between\n4.Below Min & Above Max\n5.Any Change of Value\nYour Option(1,2,3,4 or 5):\t' ))
            if ty in (1,2):
                while True:
                    try:
                        val = float(input('Higher Than:\t')) if ty==1 else float(input('Lower Than:\t'))
                        break
                    except Exception:
                        print('Value Error. Enter Valid Floating Point Number')
                break
            elif ty in (3,4):
                while True:
                    try:
                        val = [float(i) for i in input('Between (a,b). Enter a,b:\t').split(',')] if ty==3 else [float(i) for i in input('Enter min, max:\t').split(',')]
                        break
                    except Exception:
                        print('Value Error. Enter Valid Floating Point Numbers')

                if ty==3 and val[0]==val[1]:
                    print(f'Nothing Between {val[0]} and {val[1]}')
                    raise
                if ty==4 and val[0]>val[1]:
                    print(f'\nWARNING!!\nGiven:\tMin({val[0]}), Max({val[1]})\nAltered:\tMin({val[1]}), Max({val[0]})\nIf above {val[1]} and below {val[0]} is required, close this and select option 3.\n')
                val.sort()

                break
            elif ty == 5:
                val = None
                break
            else:
                raise
        except Exception:
            print('Invalid Input. Retry.')
    return ty, val
```
#### 3/5 [DataScrapper.py](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/Scripts/DataScrapper.py)
Functions for scrapping the data from the Money-Control site are present in this module.
```python
import requests
import json
from bs4 import BeautifulSoup

def ListOfShares():
    hrefs = dict()
    for i in range(65, 91):
        page = requests.Session().get('https://www.moneycontrol.com/india/stockpricequote/'+chr(i))
        parsedpage = BeautifulSoup(page.text, 'html.parser')
        tags = parsedpage.find_all(class_='bl_12')

        for tag in tags:
            try:
                if tag['href'].startswith('http'):
                    hrefs[tag.text] = {'key': tag['href'].rsplit('/', 1)[-1], 'url': tag['href']}
            except Exception:
                pass

    return hrefs

def getvalues(key):
    BSE = lambda: float(json.loads(requests.Session().get('http://priceapi-aws.moneycontrol.com/pricefeed/bse/equitycash/'+key).text)['data']['pricecurrent']) if int(json.loads(requests.Session().get('http://priceapi-aws.moneycontrol.com/pricefeed/bse/equitycash/'+key).text)['code']) == 200 else 'NA'
    NSE = lambda: float(json.loads(requests.Session().get('http://priceapi-aws.moneycontrol.com/pricefeed/nse/equitycash/'+key).text)['data']['pricecurrent']) if int(json.loads(requests.Session().get('http://priceapi-aws.moneycontrol.com/pricefeed/nse/equitycash/'+key).text)['code']) == 200 else 'NA'

    return BSE(), NSE()
```
#### 4/5 [Operations.py](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/Scripts/Operations.py)
The logical functionalities like selecting the value whether to display, prompt a notification, etc. are done in the module.
```python
import DataScrapper as ds
import time
from win10toast import ToastNotifier


values = {'Name': '-1', 'BSE': 'NA', 'NSE': 'NA', 'Time': str(time.strftime('%d-%b-%y %H:%M:%S'))}
collection = []

def logic(BSE, NSE, ft, lowerThan, higherThan):
    flag = False
    if lowerThan == higherThan == -1:
        flag = True
    elif lowerThan != -1 and higherThan == -1:
        if BSE != 'NA' and NSE != 'NA':
            if BSE < lowerThan or NSE < lowerThan:
                flag = True
        elif BSE != 'NA' and NSE == 'NA':
            if BSE < lowerThan:
                flag = True
        elif BSE == 'NA' and NSE != 'NA':
            if NSE < lowerThan:
                flag = True
    elif lowerThan == -1 and higherThan != -1:
        if BSE != 'NA' and NSE != 'NA':
            if BSE > higherThan or NSE > higherThan:
                flag = True
        elif BSE != 'NA' and NSE == 'NA':
            if BSE > higherThan:
                flag = True
        elif BSE == 'NA' and NSE != 'NA':
            if NSE > higherThan:
                flag = True
    else:
        if ft==3:
            if BSE != 'NA' and NSE != 'NA':
                if (BSE > higherThan or NSE > higherThan) and (BSE < lowerThan or NSE < lowerThan):
                    flag = True
            elif BSE != 'NA' and NSE == 'NA':
                if BSE > higherThan and BSE < lowerThan:
                    flag = True
            elif BSE == 'NA' and NSE != 'NA':
                if NSE > higherThan and NSE < lowerThan:
                    flag = True
        elif ft==4:
            if BSE != 'NA' and NSE != 'NA':
                if (BSE > higherThan or NSE > higherThan) or (BSE < lowerThan or NSE < lowerThan):
                    flag = True
            elif BSE != 'NA' and NSE == 'NA':
                if BSE > higherThan or BSE < lowerThan:
                    flag = True
            elif BSE == 'NA' and NSE != 'NA':
                if NSE > higherThan or NSE < lowerThan:
                    flag = True
    return flag

def NotificationLogger(share, ft, vals):

    global values
    global collection

    if ft in (3,4):
        lowerThan, higherThan = vals if ft==4 else reversed(vals)
    elif ft in (1, 2):
        lowerThan, higherThan = (-1, vals) if ft==1 else (vals, -1)
    else:
        lowerThan, higherThan = -1, -1

    toaster = ToastNotifier()
    toast = lambda name, bse, nse: toaster.show_toast(name, f'BSE: {bse}\tNSE: {nse}', icon_path="Includes\\Stocks Icon.ico", duration=0)

    while True:
        BSE , NSE = ds.getvalues(share['key'])
        time_of_call = str(time.strftime('%d-%b-%y %H:%M:%S'))
        print(f'\nShare:\t{share["name"]}\nBSE:\t{BSE}\nNSE:\t{NSE}\nAt:\t{time_of_call}\n\nPress CTRL+C (in Console) or CTRL+I (in Shell) to Exit')

        if values['BSE'] != BSE or values['NSE'] != NSE:
            values['Name'] = share['name']
            values['BSE'] = BSE
            values['NSE'] = NSE
            values['Time'] = time_of_call
            collection.append(values)

            if logic(BSE, NSE, ft, lowerThan, higherThan):
                toast(share['name'], BSE, NSE)
```
#### 5/5 [SaveLogs.py](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/Scripts/SaveLogs.py)
Finally, when the execution is interrupted, the logs of the session are saved to local directory using the function present in this module.
```python
import Operations as op
import os, time

def save_logs(collection):
    if len(collection) == 0:
        return False
    else:
        if not os.path.isdir('Logs'):
            os.mkdir('Logs')
        with open(os.path.join(os.getcwd(), 'Logs', 'SPN_Logs_'+time.strftime('%d%b%y%H%M%S').upper()+'.txt'), 'w') as f:
            [f.writelines(f'Share: {line["Name"]}\tBSE: {line["BSE"]}\tNSE: {line["NSE"]}\tAt {line["Time"]}\n') for line in collection]
            f.close()
        return f.name
```

### [Sample Output](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/Samples/Sample%20Output.txt) :bar_chart:
```
Microsoft Windows [Version 10.0.17134.1425]
(c) 2018 Microsoft Corporation. All rights reserved.

H:\Projects\Python Related Stuff\Pyzo Projects\ShareMarketStuff\Share_Price_Notifier\SharePriceNotifier 1.2.0>SharePriceNotifier.exe
There are a total of 8640 shares. To make the selection simple, use the followning option:
1. Specific Alphabet's Shares.
2. Else, All Shares.

Your Option? [1, 2]     1
Great! Now Enter The Letter (Case-Insensitive) You Want to Shortlist. Your Letter? [A-Z]        y
Your Letter is Y

List of 'Y' Shares:
Sno.    Name
1       Yama Polymers
2       Yamini Invt
3       Yangir Syntheti
4       Yantra Natural
5       Yarn Syndicate
6       Yash Chemex
7       Yash Manage
8       YASH PAKKA LTD
9       Yash Trading
10      Yasho Industrie
11      Yashraj Contain
12      Yenepoya Minera
13      Yes Bank
14      Yogi Pharmacy
15      Yogi Polyesters
16      Yogi-Sung-Won
17      Yogindera
18      Yokogawa India
19      York Exports
20      YS Porcelain
21      Yug Decor
22      Yuken India
23      Yule Financing
24      Yuranus Infra
25      Yuvraaj Hygiene
26      Yuvraj Intl

Your Share [1,26]:      13

Great! You've Selected Yes Bank


Yes Bank's present BSE, NSE values are (27.25, 27.25)
You can Cross-Check from http://www.moneycontrol.com/india/stockpricequote/banksprivatesector/yesbank/YB

Please Select Type of Alert (Applies for both BSE and NSE)
1.Higher Than
2.Less Than
3.Between
4.Below Min & Above Max
5.Any Change of Value
Your Option(1,2,3,4 or 5):      3
Between (a,b). Enter a,b:       20, 30

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:35

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:36

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:36

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:37

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:37

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:37

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:38

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:39

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:39

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:40

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:41

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:41

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:42

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:42

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:43

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:43

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:43

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:44

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:45

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:45

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:45

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

Share:  Yes Bank
BSE:    27.25
NSE:    27.25
At:     29-Apr-20 02:30:46

Press CTRL+C (in Console) or CTRL+I (in Shell) to Exit

--Interrupted--

Your Notification's Log is Saved At:
H:\Projects\Python Related Stuff\Pyzo Projects\ShareMarketStuff\Share_Price_Notifier\SharePriceNotifier 1.2.0\Logs\SPN_Logs_29APR20023108.txt

Press Any Key to Exit.

H:\Projects\Python Related Stuff\Pyzo Projects\ShareMarketStuff\Share_Price_Notifier\SharePriceNotifier 1.2.0>
```

### [Executable File](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/SharePriceNotifier.exe) :floppy_disk:
_[Executable](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/SharePriceNotifier.exe) for using in change of configuration of base system or in absence of python. The file can be used for distribution with ease and without dependencies. Following are the commands used to create the executable file. [Click here](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/Freezing%20Logs.txt) for freezing logs._

#### Creating Specifications file :page_facing_up:
```
pyi-makespec --onefile  --hidden-import=DataScrapper --hidden-import=User_Inputs --hidden-import=Operations --hidden-import=SaveLogs --hidden-import=requests --hidden-import=json --hidden-import=bs4 --hidden-import=os --hidden-import=time --hidden-import=win10toast --hidden-import=pkg_resources.py2_warn --icon=".\Includes\Stocks Icon.ico" --specpath="H:\Projects\Python Related Stuff\Pyzo Projects\ShareMarketStuff\Share_Price_Notifier\SharePriceNotifier 1.2.0" ".\Scripts\SharePriceNotifier.py"
```

This creates the [MagPi-Fetch.spec](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/SharePriceNotifier.spec) as follows,
```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Scripts\\SharePriceNotifier.py'],
             pathex=['H:\\Projects\\Python Related Stuff\\Pyzo Projects\\ShareMarketStuff\\Share_Price_Notifier\\SharePriceNotifier 1.2.0'],
             binaries=[],
             datas=[],
             hiddenimports=['DataScrapper', 'User_Inputs', 'Operations', 'SaveLogs', 'requests', 'json', 'bs4', 'os', 'time', 'win10toast', 'pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SharePriceNotifier',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='Includes\\Stocks Icon.ico')
```

#### Creating Executable :arrow_forward:

PyPI `Pyinstaller 3.6` was used to create the executable in PIP environment. Command as follows,
```
pyinstaller --onefile  --hidden-import=DataScrapper --hidden-import=User_Inputs --hidden-import=Operations --hidden-import=SaveLogs --hidden-import=requests --hidden-import=json --hidden-import=bs4 --hidden-import=os --hidden-import=time --hidden-import=win10toast --hidden-import=pkg_resources.py2_warn --icon=".\Includes\Stocks Icon.ico" --specpath="H:\Projects\Python Related Stuff\Pyzo Projects\ShareMarketStuff\Share_Price_Notifier\SharePriceNotifier 1.2.0" ".\Scripts\SharePriceNotifier.py"
```

### Other Useful Things :bank:
1. [Samples](https://github.com/Bhargav43/ShareMarketStuff/tree/master/SharePriceNotifier%201.2.0/Samples): Contains the HTML page samples of some of the URLs that are hit during the data scrapping, sample output, etc.
1. [Directory Structure](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/Directory%20Structure.txt): Contains the list of pages and the residing directory structure of this project so nothing misses off. Note: This excludes Logs directory as they aren't mandatory.
1. [Includes](https://github.com/Bhargav43/ShareMarketStuff/tree/master/SharePriceNotifier%201.2.0/Includes): Contains the Icon file used for the executable.
1. [Logs](https://github.com/Bhargav43/ShareMarketStuff/tree/master/SharePriceNotifier%201.2.0/Logs) Collects the logs of the past executions. This may be deleted as a whole when isn't required. Program creates directory when executed.

### Finally, the Working Model :metal:

Click for accessing [SharePriceNotifier.exe](https://github.com/Bhargav43/ShareMarketStuff/blob/master/SharePriceNotifier%201.2.0/SharePriceNotifier.exe)

# Farewell! :tada::tada:
