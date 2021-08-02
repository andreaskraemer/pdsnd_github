import time
import pandas as pd
import numpy as np

CITY_DATA = { 'c': 'chicago.csv',
              'n': 'new_york_city.csv',
              'w': 'washington.csv' }
MONTH_LIST = ['dummy', 'January', 'February', 'March', 'April', 'May', 'June']
WEEK_DAY_LIST = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - first character of the name of the city to analyze, i.e c=chicago, n=new york city or w=washington
        (int) month - number of the month (1=Jan, 2=Feb, 3=Mar, 4=Apr, 5=May, 6=Jun) to filter by, or "-1" to apply no month filter)
        (int) day - name of the day of week (0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun) to filter by, or "-1" to apply no day filter)
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (c=chicago, n=new york city or w=washington). 
    city = input("Enter the name of the city to analyze (feasible entries are: c,C=chicago, n,N=new york city, w,W=washington): ")
    city = city.lower()
    while city not in CITY_DATA:
        print("The character that you entered is not valid. Please try again.")
        city = input("Enter the name of the city to analyze (feasible entries are: c,C=chicago, n,N=new york city, w,W=washington): ")
        city = city.lower()
        
    # get user input for month (1=Jan, 2=Feb, 3=Mar, 4=Apr, 5=May, 6=Jun, -1=all months)
    while True:
        try:
            month = int(input("Enter the (number of the) month to analyze (feasible entries are: 1=Jan, 2=Feb, 3=Mar, 4=Apr, 5=May, 6=Jun, -1=all): "))
        except:
            print("The string that you entered is not a number. Please try again.")
        else:
            if month == -1 or (month >= 1 and month <= 6):
                break
            else:    
                print("The number that you entered is not a valid month, i.e. 1,2,..,6 or -1. Please try again")

    # get user input for day of week 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun, -1= all days of the week)
    while True:
        try:
            day = int(input("Enter the (number of the) weekday to analyze (feasible entries are: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun, -1=all): "))
        except:
            print("The string that you entered is not a number. Please try again.")
        else:
            if day >= -1 and day <= 6:
                break
            else:    
                print("The number that you entered is not a valid day, i.e. 0,1,2,..,6 or -1. Please try again.")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - first character of the name of the city to analyze, i.e c=chicago, n=new york city or w=washington
        (int) month - number of the month (1=Jan, 2=Feb, 3=Mar, 4=Apr, 5=May, 6=Jun) to filter by, or "-1" to apply no month filter
        (int) day - name of the day of week (0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun) to filter by, or "-1" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != -1:
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != -1:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]

    return df

def display_raw_data(df):
    """
    Displays raw data of the dataframe interactivly. While the user confirms that she/he wants to see raw data
    5 lines of raw data are shown, i.e. line 0-4 in the fisrt step, line 5-9 in the second step, and so on
    """
    i = 0
    raw = input("\nWould you like to the first 5 lines of raw data? Please enter y,Y (for yes) or n,N (for no)\n").lower()
    pd.set_option('display.max_columns',200)

    while True and i < len(df.index):            
        if raw == 'n':
            break
        elif raw == 'y':
            # display next five rows
            print('\n')
            print(df.iloc[i:i+5,:]) 
            print('\n')
            raw = input("\nWould you like to the next 5 lines of raw data? Please enter y,Y (for yes) or n,N (for no)\n").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    num_rows = len(df.index)
    
    # extract hour from the Start Time column to create an hour column
    # df['month'] and df['day_of_week'] are already calculated
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    freq = df['month'].value_counts()
    print("Most travels ({}%) were in the month {}".format(round(freq.values[0]/num_rows*100,1), MONTH_LIST[freq.index[0]]))

    # display the most common day of week
    freq = df['day_of_week'].value_counts()
    print("Most travels ({}%) were on the weekday {}".format(round(freq.values[0]/num_rows*100,1), WEEK_DAY_LIST[freq.index[0]]))

    # display the most common start hour
    freq = df['hour'].value_counts()
    print("Most travels ({}%) started in the hour from {}:00h to {}:59h".format(round(freq.values[0]/num_rows*100,1), freq.index[0], freq.index[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    num_rows = len(df.index)

    # display most commonly used start station
    freq = df['Start Station'].value_counts()
    print("Most travels ({}%) started from {}".format(round(freq.values[0]/num_rows*100,2), freq.index[0]))

    # display most commonly used end station
    freq = df['End Station'].value_counts()
    print("Most travels ({}%) ended at {}".format(round(freq.values[0]/num_rows*100,2), freq.index[0]))

    # display most frequent combination of start station and end station trip
    freq = df.groupby(['Start Station', 'End Station']).size()
    idx_max = freq.idxmax()
    print("Most travels ({}%) are from {} to {}".format(round(freq.get(idx_max)/num_rows*100,2),idx_max[0],idx_max[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time in seconds is {}".format(round(df['Trip Duration'].sum(),1)))

    # display mean travel time
    print("Mean travel time in seconds is {}".format(round(df['Trip Duration'].mean(),1)))
    # print(type(df['Trip Duration']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for index, value in user_types.items():
            print("Bikeshare was used by {} {} Users".format(value,index))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        for index, value in gender_types.items():
            print("Bikeshare was used by {} {} Users".format(value,index))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        latest_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].value_counts().index[0]
        print("The oldest bikeshare user is born in {}".format(int(earliest_year)))
        print("The youngest bikeshare user is born in {}".format(int(latest_year)))
        print("The most common year of birth of bikeshare users is {}".format(int(most_common_year)))
        #print("earliest year of birth is {}, latest year of birth is {}, most common year of birth is {}".format(int(earliest_year), int(latest_year), int(most_common_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # determine city, month and weekday of the data that shall be evaluated
        city, month, day = get_filters()
        
        # load dat in dataframe
        df = load_data(city, month, day)
        
        # display_raw_data (if requested by the user)
        # display_raw_data(df)
        
        # calculate statistics
        if len(df.index) > 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        
        # check if another calculation shall be done
        restart = 'undefined'
        while restart.lower() != 'y' and restart.lower() != 'n':
            restart = input('\nWould you like to restart? Please enter y,Y (for yes) or n,N (for no).\n')
        if restart.lower() == 'n':
            break


if __name__ == "__main__":
	main()
