import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_available = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city you want to see the data for? Please type Chicago, New York City or Washington: ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Please try again, your input was wrong!\nWhich city you want to see the data for? Please type Chicago, New York City or Washington: ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('If you want to apply a filter by month (from January to June) please write the name of the month or else write all: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Please try again, your input was wrong!\nIf you want to apply a filter by month (from January to June) please write the name of the month or else write all: ').lower()
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('If you want to apply a filter by day please write the name of the day or else write all: ')
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Please try again, your input was wrong!\nIf you want to apply a filter by day please write the name of the day or else write all: ').lower()
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months_available.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    print('The month with the most trips is: {}\n'.format(months_available[df['month'].mode()[0] - 1]).title())
   
    # TO DO: display the most common day of week
    print('The day of the week with the most trips is: {}\n'.format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print('The hour of the day with the most trips is: {}\n'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most used start station is: {}\n'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('The most used end station is: {}\n'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print('The most common trip is: {}\n'.format(df.groupby(['Start Station','End Station']).size().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The total travel time is: {}\n'.format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print('The mean travel time is: {}\n'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = {}  
    for i in range(len(df['User Type'].value_counts())):
        user_types[df['User Type'].value_counts().keys()[i]] = df['User Type'].value_counts()[i]
    print('Showing users per type: {}\n'.format(user_types))

    # TO DO: Display counts of gender
    # Washington data is missing both gender and birth year, if Washington is selected by the user print missing info message
    if city == 'washington':
        print('There are no stats available for the gender in Washington.\n')
        print('There are no stats available for youngest or average user age for Washington.\n')
    else:
        gender = {}
        for i in range(len(df['Gender'].value_counts())):
            gender[df['Gender'].value_counts().keys()[i]] = df['Gender'].value_counts()[i]
        print('Showing users per gender: {}\n'.format(gender))

        # TO DO: Display earliest, most recent, and most common year of birth
        print('The youngest user is born in {}\n'.format(int(df['Birth Year'].max())))
        print('The average user is born in {}\n'.format(int(df['Birth Year'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Displays 5 lines of raw data for as long as the user inputs 'yes'"""
    start_line = 5
    end_line = 10
    while input('\nWould you like to view the next 5 lines of raw data? Enter yes or no: ').lower() == 'yes':
        print(df[start_line:end_line])
        start_line = end_line
        end_line += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if input('\nWould you like to view statistics on the most frequent times of travel? Enter yes or no: ').lower() == 'yes':
            time_stats(df)
        if input('\nWould you like to view statistics on the most popular stations and trip? Enter yes or no: ').lower() == 'yes':
            station_stats(df)
        if input('\nWould you like to view statistics on the total and average trip duration? Enter yes or no: ').lower() == 'yes':
            trip_duration_stats(df)
        if input('\nWould you like to view statistics on bikeshare users? Enter yes or no: ').lower() == 'yes':
            user_stats(df, city)
        if input('\nWould you like to view raw data (5 lines)? Enter yes or no: ').lower() == 'yes':
            print(df[0:5])
            show_raw_data(df)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
