import datetime


datalimite = datetime.datetime(year=2027, month=7, day=11)
hoje = datetime.datetime.now()


def check():
    return hoje < datalimite
