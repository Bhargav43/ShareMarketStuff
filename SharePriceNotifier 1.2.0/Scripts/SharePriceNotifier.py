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