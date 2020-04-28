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
