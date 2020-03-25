#---------------------------------------------------------------------------------------------------------
#Load Libraries ---------- -------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import calendar as cd
import datetime as dt

CITIES = {'CH': 'chicago',
          'NY': 'new york city',
          'WS': 'washington'}

DAYS = {'MON':'Monday',
        'TUE':'Tuesday',
        'WED':'Wednesday',
        'THU':'Thursday',
        'FRI':'Friday',
        'SAT':'Saturday',
        'SUN':'Sunday'}


# A user input checker, used multiple times
def yn_check(x):
    """
    Loops through until user selects either y or n
    Arg = user input

    """
    while True:
        if x.upper() not in ['Y','N']:
            x = input("Please try again: ")
        else:
            break
    return x



#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
""" MAIN CODE STARTS FROM HERE """

def file_choices():

    """
    Function to gather user inputs, to pick file and apply any filters
    Arg = none
    Output = city, month and day of week file inputs

    """


# User Input to Choose City -------------------------------------------------------------------------------
    city = input("Which city would you like to look at? Chicago (CH), New York City (NY) or Washington (WS)? >>> ")

    while True:
        if city.upper() not in CITIES:
            city = input("I'm sorry, that wasn't one of the options.  Please enter CH, NY or WS >>> ")
        else:
            city = CITIES[city.upper()]
            print("Thank you, you have chosen to look at {}".format(city.title()))
            break



# User Input to Choose Month ------------------------------------------------------------------------------
    temp = input("Would you like to include all months of data? Y/N >>> ")
    temp = yn_check(temp)

    if temp.upper() == 'Y':
        print("You have chosen to look at all months")
        month = 0
    else:
        while True:
            try:
                month = int(input('Pick a number between 1-6 (1=Jan,2=Feb,...,6=Jun) >>> '))
            except ValueError:
                print('That\'s not a valid number!')
            else:
                if 1 <= month <= 6:
                    m = cd.month_name[month] #for the full name
                    print("Thank you, you have chosen to look at {}".format(m))
                    break
                else:
                    print('That\'s not a valid number!')



# User Input to Choose Day --------------------------------------------------------------------------------
    day = input("Would you like to include all days of the week in results? Y/N >>> ")
    day = yn_check(day)

    if day.upper() == "N":
        print("Note these are the day formats {}".format(DAYS))
        day = input("Please choose a day >>> ")
        while True:
            if day.upper() not in DAYS:
                day = input("I'm sorry, that wasn't one of the options.  Please try again >>> ")
            else:
                day = DAYS.get(day.upper())
                print("Thank you, you have chosen to look at {}".format(day.title()))
                break


    return city, month, day


#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------

##---------------------------------------------------------------------------------------------------------
## Open the correct csv file ------------------------------------------------------------------------------
def load_data(c,m,d):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 0 to apply no month filter
        (str) day - name of the day of week to filter by, or Y to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #Load data into dataframe
    fname = c.replace(" ","_") + ".csv"
    df = pd.read_csv(fname)

    #Convert the start time to date
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Create Start & End Station Column
    df['Journey'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']

    # Create duration time column
    df['Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds()

    # filter by month if applicable
    if m != 0:
        df = df[df['month'] == m]

    # filter by day of week if applicable
    if d.upper() != 'Y':
        df = df[df['day_of_week'] == d.title()]

    # Fill in missing values
    df['User Type'].fillna('Unknown')

    # Print sum statistics on missing values
    x = pd.isnull(df).sum()
    print("\nThese are the number of missing rows per column\n{}".format(x))

    return df


#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------

##---------------------------------------------------------------------------------------------------------
# Display first five rows of data, and next 5 until user stops
def display(df):

    """
    Allows user to view 5 rows of data at a time until they choose to stop, or max rows is reached
    Args = dataframe
    """

    # Create column of row numbers & find last row index
    df['Row'] = np.arange(len(df))
    end = df.count()[0]

    n = 0

    user = input("Would you like to see the first 5 rows? (Y/N) >>> ")
    y = yn_check(user)

    # Loop through until user chooses to terminate, or the max number of rows is reached
    while True:
        if y.upper() != 'Y':
            break
        elif n > end:
            print("No more rows to display")
            break
        else:
            print(df.iloc[n:min((n+5),end)])

        y = input("Would you like to see the next 5 rows? (Y/N) >>> ")
        y = yn_check(y)
        n += 5


#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
# Q1 Modal Values for Dates/Time
def modal_dt(x):
    """
    Function to calculate how many of a certain time period there are in a given number of seconds
    Args - tot    = total number of seconds to look at
         - period = number of seconds in a given period

    Returns x, the whole number of time period, and y, the remaining number of seconds
    """
    occ = df[x].value_counts().iloc[0]
    mod = df[x].mode()[0]

    if x == 'month':
        temp = cd.month_name[mod]
    else:
        temp = mod
    return print("\nRESULT: The most common {} is {}, with {:,} occurences".format(x.replace('_',' '),temp,occ))
# formatting trick found online for putting a comma in to separate thousands


#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
# Q2 Modal Values for Stations Function
def modal_st(x):
    """
    Function to calculate the modal value of a given column in a dataframe
    Arg = column to look at
    Returns the modal catagory and the number of occurences
    """
    occ = df[x].value_counts().iloc[0]
    mod = df[x].value_counts().idxmax()

    return print("\nRESULT: The most common {} is {}, with {:,} occurences".format(x.replace('_',' ').lower(),mod,occ))


#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
# Q3 Trip Durations

def time_span(tot,period):
    """
    Function to calculate how many of a certain time period there are in a given number of seconds
    Args - tot    = total number of seconds to look at
         - period = number of seconds in a given period

    Returns x, the whole number of time period, and y, the remaining number of seconds
    """

    x = tot // period
    if x == 0:
        y = tot
    else:
        y = tot % (x * period)
    return x, y


#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
# Run the code to generate output

while True:

    file_inputs = file_choices()
    df = load_data(file_inputs[0],file_inputs[1],file_inputs[2])
    y = display(df)

    #---------------------------------------------------------------------------------------------------------
    # Q1 Popular Times of Travel

    z = modal_dt('month')
    z = modal_dt('day_of_week')
    z = modal_dt('hour')


    #---------------------------------------------------------------------------------------------------------
    # Q1 Popular Stations for Travel

    z = modal_st('Start Station')
    z = modal_st('End Station')
    z = modal_st('Journey')


    #---------------------------------------------------------------------------------------------------------
    # Q3.1 Total Travel Time

    # Calculate the number of seconds for given time periods
    secs_sc = 1
    secs_mn = secs_sc * 60
    secs_hr = secs_mn * 60
    secs_dy = secs_hr * 24
    secs_wk = secs_dy * 7
    secs_yr = secs_dy * 365.25
    secs_mt = secs_yr / 12

    # Total number of durtaions seconds over dataset
    tot = np.nansum(df['Duration'])

    periods = [secs_yr,secs_mt,secs_wk,secs_dy,secs_hr,secs_mn,secs_sc]
    results = []

    # Loop through different periods to print how many of each there have been
    for i in periods:
        out = int(time_span(tot,i)[0])
        tot = time_span(tot,i)[1]
        results.append(out)

    print("\nRESULT: Total travel time = {} years, {} months, {} weeks, {} days, {} hours, {} minutes and {} seconds".format(\
    results[0],results[1],results[2],results[3],results[4],results[5],results[6]))


    #---------------------------------------------------------------------------------------------------------
    # Q3.2 Average Travel Time

    # Average Duration
    tot = int(df['Duration'].mean())

    periods = [secs_hr,secs_mn,secs_sc]
    results = []

    # Loop through different periods to print how many of each there have been
    for i in periods:
        out = int(time_span(tot,i)[0])
        tot = time_span(tot,i)[1]
        results.append(out)

    print("\nRESULT: Average travel time = {} hours, {} minutes and {} seconds".format(\
    results[0],results[1],results[2]))


    #---------------------------------------------------------------------------------------------------------
    # Q4.1 Counts of each user type
    print("\nRESULT: Counts of user type.. \n{}".format(df.groupby(['User Type'])['Row'].count()))

    # Q4.2 & 4.3
    if file_inputs[0] != 'washington':
        # Counts of gender
        print("\nRESULT: Counts of gender.. \n{}".format(df.groupby(['Gender'])['Row'].count()))
        # Earliest year of birth
        print("\nRESULT: Earliest year of birth is {}".format(int(df['Birth Year'].min())))
        # Most common year of birth
        print("\nRESULT: Most common year of birth is {}".format(int(df['Birth Year'].mode()[0])))
        # Most recent year of birht
        print("\nRESULT: Most recent year of birth is {}".format(int(df['Birth Year'].max())))

    # User option to restart the code
    restart = input('\nWould you like to restart? (Y/N) >>> ')
    restart = yn_check(restart)

    # Quit if user chooses to
    if restart.upper() != 'Y':
        print("Thank you, goodbye")
        break
  
