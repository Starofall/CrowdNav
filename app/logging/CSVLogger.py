import csv

from app import Config

csv.register_dialect('custom', doublequote=False, quoting=csv.QUOTE_NONE)


def logEvent(file, row):
    try:
        with open('./data/' + str(file) + '_' + str(Config.processID) + '.csv', 'ab') as mycsvfile:
            writer = csv.writer(mycsvfile, dialect='excel')
            writer.writerow(row)
    except:
        pass