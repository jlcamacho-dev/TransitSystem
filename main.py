import pandas as pd
import urllib.parse as up
import psycopg2
import datetime

pd.set_option('display.width', 1000)


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")


# ---------------  DB Connection -----------------------------------------#
def connect():
    db_name = 'oscugeoe'
    db_pass = None # database key/pass goes here, ommitted for security reasons 
    db_server = 'drona.db.elephantsql.com'
    up.uses_netloc.append('postgres')
    conxn = psycopg2.connect(database=db_name, user=db_name, password=db_pass, host=db_server, port='5432')

    if conxn:
        print('Connected Successfully!')
    else:
        print('Error')
    return conxn


# --------------- delete methods --------------------#
def delbus(fcon):
    busID = input('Plesae enter bus id you wish to delete: ')
    try:
        busID = int(busID)
    except ValueError:
        print('Invalid input...')

    sql = f'DELETE FROM Bus WHERE BusID = {busID};'

    try:
        cur = fcon.cursor()
        cur.execute(sql)
        fcon.commit()
        cur.close()
        print('Changed Successfully!')
    except Exception as err:
        print(f'ERROR exception type: {err}')
    return fcon


def delTrip(fcon):
    tNumber = input('Please enter trip number: ')
    cdate = input('Please enter date in YYYY-MM-DD: ')
    validate(cdate)
    ssTime = input('Please enter scheduled start time: ')

    try:
        tNumber = int(tNumber)
        ssTime = int(ssTime)
    except ValueError:
        print('invalid input...')

    sql = f'DELETE FROM TripOffering WHERE TripNumber = {tNumber} AND DateOp = \'{cdate}\' AND ScheduledStartTime = {ssTime};'
    try:
        cur = fcon.cursor()
        cur.execute(sql)
        fcon.commit()
        cur.close()
        print('Processed Successfully!')
    except Exception as err:
        print(f'ERROR exception type: {err}')
    return fcon


# --------------- Change methods --------------------#
def changeDriver(fcon):
    dName = input('Please enter desired drivers name to change: ')
    newName = input('Please enter the name to change to: ')
    tNumber = input('Please enter trip number: ')
    cdate = input('Please enter date in YYYY-MM-DD: ')
    validate(cdate)
    ssTime = input('Please enter scheduled start time: ')

    try:
        ssTime = int(ssTime)
    except ValueError:
        print('incorrect value for scheduled start time..')

    sql = f'UPDATE TripOffering SET DriverName = \'{newName}\' WHERE TripNumber = {tNumber} AND ScheduledStartTime = {ssTime} AND DriverName = \'{dName}\' AND DateOp = \'{cdate}\';'


    try:
        cur = fcon.cursor()
        cur.execute(sql)
        fcon.commit()
        cur.close()
        print('Changed Successfully!')
    except Exception as err:
        print(f'ERROR exception type: {err}')
    return fcon


def changeBus(fcon):
    tripNumber = input('Please enter trip number: ')
    busID = input('Please enter bus ID to change: ')
    newBusID = input('Please enter new bus ID to change to: ')

    try:
        busID = int(busID)
        newBusID = int(newBusID)
    except ValueError:
        print('Invalid bus id..')

    sql = f'UPDATE TripOffering SET BusID = {newBusID} WHERE TripNumber = {tripNumber}'

    try:
        cur = fcon.cursor()
        cur.execute(sql)
        fcon.commit()
        cur.close()
        print('Changed Successfully!')
    except Exception as err:
        print(f'ERROR exception type: {err}')
    return fcon


# --------------- Add methd -------------------------#
def tripOffering(fcon):

    bVal = True
    tripNumber = list()
    busID = list()
    driverName = list()
    dateop = list()
    sTime = list()
    eTime = list()

    # request user input
    while bVal:
        tmp = input('Please enter Trip Number: ')
        tripNumber.append(tmp)
        tmp = input('Please enter Bus ID: ')
        busID.append(tmp)
        tmp = input('Please enter Driver Name: ')
        driverName.append(tmp)
        tmp = input('Please enter date in YYYY-MM-DD: ')
        dateop.append(tmp)
        tmp = input('Please input start time (numeric whole number 1-24): ')
        sTime.append(tmp)
        tmp = input('Please input end time (numeric whole number 1-24): ')
        eTime.append(tmp)
        resp = input('Continue? y/n: ')
        if resp == 'n':
            bVal = False

    # validate user input
    for i in range(len(tripNumber)):
        try:
            tripNumber[i] = int(tripNumber[i])
        except ValueError:
            print(f'trip number {tripNumber[i]} invalid')
        try:
            busID[i] = int(busID[i])
        except ValueError:
            print(f'bus id {busID[i]} invalid')
        validate(dateop[i])
        try:
            sTime[i] = int(sTime[i])
            eTime[i] = int(eTime[i])
        except ValueError:
            print('invalid time')

    cur = fcon.cursor()
    # curate and comit input to sql
    for i in range(len(tripNumber)):
        v1 = tripNumber[i]
        v2 = busID[i]
        v3 = driverName[i]
        v4 = dateop[i]
        v5 = sTime[i]
        v6 = eTime[i]

        data = (v1, v2, v3, v4, v5, v6)
        sql = 'INSERT INTO TripOffering (TripNumber, BusID, DriverName, DateOp, ScheduledStartTime, ' \
              'ScheduledArrivalTime) VALUES (%s, %s, %s, %s, %s, %s); '
        try:
            cur.execute(sql, data)
            fcon.commit()
            print('Added Successfully!')
        except Exception as err:
            print(f'ERROR exception type: {err}')
    cur.close()
    return fcon


def bus(fcon, idNum, make, year):
    '''
    INSERT INTO Bus (BusID, Model, year)
    VALUES (23, 'Ford', 1930);
    '''

    try:
        year = int(year)
        idNum = int(idNum)
    except ValueError:
        print('Input not valid..')
        return fcon
    data = (idNum, make, year)
    sql = 'INSERT INTO Bus (BusID, Model, year) VALUES (%s, %s, %s);'
    try:
        cur = fcon.cursor()
        cur.execute(sql, data)
        fcon.commit()
        cur.close()
        print('Added Successfully!')
    except Exception as err:
        print(f'ERROR exception type: {err}')
    return fcon


def driver(fcon, name, number):
    '''
    INSERT INTO Driver (DriverName, DrivePhoneNumber)
    VALUES ('Peggy', 265);
    '''
    try:
        number = int(number)
    except ValueError:
        print('Number was not accepted...')
        return fcon

    data = (name, number)
    sql = 'INSERT INTO Driver(DriverName, DrivePhoneNumber) VALUES (%s, %s);'

    try:
        cur = fcon.cursor()
        cur.execute(sql, data)
        fcon.commit()
        cur.close()
        print('Added Successfully!')
    except Exception as err:
        print(f'ERROR exception type: {err}')
    return fcon


def addTripStop(fcon):
    '''
    INSERT INTO ActualTripStopInfo (TripNumber, StopNumber, BusID, DriverName, Dateop, ScheduledStartTime, ScheduledArrivalTime, ActualStartTime, ActualArrivalTime, numberofpassengersin, numberofpassengersout)
    VALUES (%s, %s, %s, '%s, %s, %s, %s, %s, %s, %s, %s);
    '''
    # Prompt for user input
    tNumber = input('Please enter trip number: ')
    stopNumber = input('Please enter Stop Number: ')
    buID = input('Please input bus id: ')
    drName = input('Please enter driver name: ')
    date = input('Please enter desired date(YYYY-MM-DD): ')
    ssTime = input('Please input scheduled start time(1-24): ')
    saTime = input('Please input schedueld arrival time(1-24): ')
    asTime = input('Please enter actual arrival time (1-24): ')
    aaTime = input('Please input actual arrival time (1-24): ')
    poIn = input('Please enter number of passengers in: ')
    poOut = input('Please enter number of passengers out: ')

    # Process data
    try:
        tNumber = int(tNumber)
        stopNumber = int(stopNumber)
        buID = int(buID)
        validate(date)
        ssTime = int(ssTime)
        saTime = int(saTime)
        asTime = int(asTime)
        aaTime = int(aaTime)
        poIn = int(poIn)
        poOut = int(poOut)
    except ValueError:
        print('Error in input..')

    # process sql command and data
    data = (
        tNumber,
        stopNumber,
        buID,
        drName,
        date,
        ssTime,
        saTime,
        asTime,
        aaTime,
        poIn,
        poOut
        )
    sql = 'INSERT INTO ActualTripStopInfo (TripNumber, StopNumber, BusID, DriverName, Dateop, ScheduledStartTime, ' \
          'ScheduledArrivalTime, ActualStartTime, ActualArrivalTime, numberofpassengersin, numberofpassengersout) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); '

    try:
        cur = fcon.cursor()
        cur.execute(sql, data)
        fcon.commit()
        cur.close()
        print('Added Successfully!')
    except Exception as err:
        print(f'ERROR exception type: {err}')
    return fcon


# --------------- View methd -------------------------#
def viewTripOffering(fcon, start, end, date):
    sql = f'SELECT ' \
          f'tr.TripNumber, ' \
          f'tr.StartLocationName, ' \
          f'tr.DestinationName, ' \
          f'tro.DateOp, ' \
          f'tro.ScheduledStartTime, ' \
          f'tro.ScheduledArrivalTime, ' \
          f'tro.BusID, ' \
          f'tro.DriverName ' \
          f'FROM Trip tr, TripOffering tro ' \
          f'WHERE tr.TripNumber = tro.TripNumber AND ' \
          f'tr.StartLocationName LIKE \'{start}\' AND ' \
          f'tr.DestinationName LIKE \'{end}\' AND ' \
          f'tro.Dateop LIKE \'{date}\' '

    try:
        dat = pd.read_sql(sql, fcon)
        print(dat)

    except Exception as err:
        print(f'ERROR exception type: {err}')

    return fcon


def displayStops(fcon, tripNumber):
    sql = f'SELECT * FROM ActualTripStopInfo WHERE TripNumber = {tripNumber}'
    try:
        dat = pd.read_sql(sql, fcon)
        print(dat)
    except Exception as err:
        print(f'ERROR exception type: {err}')
    return fcon


def displayDriverSchedule(fcon, name):
    sql = f'SELECT ' \
          f'tro.DriverName,' \
          f'tro.Dateop, ' \
          f'tro.ScheduledStartTime, ' \
          f'tro.ScheduledArrivalTime, ' \
          f'tr.StartLocationName, ' \
          f'tr.DestinationName ' \
          f'FROM TripOffering tro, Trip tr ' \
          f'WHERE ' \
          f'tro.DriverName LIKE \'{name}\' AND ' \
          f'tro.TripNumber = tr.TripNumber; '
    try:
        dat = pd.read_sql(sql, fcon)
        print(dat)
    except Exception as err:
        print(f'ERROR exception type: {err}')
    return fcon


def menu(fcon):
    uInput = 0
    bVal = True

    while bVal:
        # Initial Menu Screen
        print('Transit Menu:')
        print('1) Add\n2) Delete\n3) Display\n4) Change\n5) Exit')
        uInput = input('Please input a number to select an option: ')

        # check user input
        try:
            uInput = int(uInput)
        except ValueError:
            print('Error incorrect input...')

        if uInput == 5:
            print('Goodbye!')
            bVal = False
        elif uInput > 5:
            print('Incorrect input...')
        elif uInput == 1:
            # add
            print('Add Options')
            print('1)Trip Offering\n2) Bus\n3) Driver\n4) Insert Trip Stop data')
            aInput = input('Please input a number to select an option: ')

            try:
                aInput = int(aInput)
            except ValueError:
                print('Error invalid input')
                break

            if aInput <= 4:
                if aInput == 1:
                    fcon = tripOffering(fcon)
                elif aInput == 2:
                    bID = input('Please enter desired id number: ')
                    model = input('Please enter model: ')
                    year = input('Please enter year in YYYY formate: ')
                    fcon = bus(fcon, bID, model, year)
                elif aInput == 3:
                    name = input('Please enter desired name: ')
                    num = input('Please enter phone number in 00000 format: ')
                    fcon = driver(fcon, name, num)
                elif aInput == 4:
                    fcon = addTripStop(fcon)

        elif uInput == 2:
            # delete
            print('Delete Options:')
            print('1) Trip Offerings\n2) Bus')
            deInput = input('Please input a number to select an option: ')

            try:
                deInput = int(deInput)
            except ValueError:
                print('Error')
                break

            if deInput <= 2:
                if deInput == 1:
                    fcon = delTrip(fcon)
                elif deInput == 2:
                    fcon = delbus(fcon)

        elif uInput == 3:
            # display
            print('Viewing Options:')
            print('1) Trip Offering\n2) Driver Schedule\n3) Stops')
            dInput = input('Please input a number to select an option: ')

            try:
                dInput = int(dInput)
            except ValueError:
                print('Error')

            if dInput <= 3:
                if dInput == 1:
                    start = input('Please enter desired starting point: ')
                    end = input('Please enter desired ending point: ')
                    date = input('Please enter desired date in YYYY-MM-DD: ')
                    fcon = viewTripOffering(fcon, start, end, date)
                elif dInput == 2:
                    dname = input('Please entered desired bus drivers name: ')
                    fcon = displayDriverSchedule(fcon, dname)
                elif dInput == 3:
                    tripNumber = input('Please entered trip number: ')
                    fcon = displayStops(fcon, tripNumber)

        elif uInput == 4:
            # change menu
            print('1) Change Driver\n2) Change Bus')
            cInput = input('Please input a number to select an option: ')
            try:
                cInput = int(cInput)
            except ValueError:
                print('Error')
            if cInput == 1:
                fcon = changeDriver(fcon)
            elif cInput == 2:
                fcon = changeBus(fcon)

    return fcon


def main() -> None:
    fcon = connect()
    fcon = menu(fcon)
    fcon.close()
    # viewTripOffering(fcon, 'Walnut', 'Pomona', '2019-02-01')


if __name__ == '__main__':
    main()
