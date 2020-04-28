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