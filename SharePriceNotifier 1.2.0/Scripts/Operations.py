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


