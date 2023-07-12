import time
import pandas as pd
import numpy as np
from datetime import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    # get user input for city (chicago, new york city, washington)
    while True:
            city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
            print()
            if city.lower() in ('chicago', 'new york city', 'washington'):
                break
            else:
                print('\nOops! That\'s not a valid input. Let\'s try again.\n')



    # get user input for month (all, january, february, ... , june)
    while True:
            month = input('Which month would you to filter by? Choose January, February, March, April, May, June? Or type "none" for no month filters.\n').lower()
            print()
            if month.lower() in ('january', 'february', 'march', 'april', 'may', 'june', 'none'):
                break
            else:
                print('\nThat\'s not a valid input. Please try again. \n ')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input('Which day of the week would you like to filter by? Choose Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday. Or type in "none" for no day filters.\n').lower()
            print()
            if day.lower() in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'none'):
                break
            else:
                print('\nThat\'s not a valid input. Let\'s try again.\n')



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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A').str.lower()

    if month != 'none':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]

    if day != 'none':
        df = df[df['day_of_week'] == day.lower()]

    print()
    print('The CITY you chose to research was {}'.format(city.upper()))
    print('The MONTH you chose to filter by, where January = 1, was {}'.format(month))
    print('The DAY you chose to filter by was {}'.format(day.upper()))
    print()
    print('-'*40)
    print()


    return df




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print()
    print()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month to rent a bike, where January = 1, is {}'.format(common_month))
    print()

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0].title()
    print('The most common day of the week to rent a bike is {}'.format(common_day))
    print()

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour of the day to rent a bike is {}'.format(common_hour))
    print()

    # display the amount of time it took to run statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print()
    print()

    start_station = df['Start Station']
    end_station = df['End Station']

    # display most commonly used start station and the number of occurrences for this station
    common_start_station = start_station.mode()[0]
    start_station_count = 0
    for station in start_station:
        if station == common_start_station:
            start_station_count += 1

    print('The most popular start station is {}. \nThis station was used {} times.'.format(common_start_station, start_station_count))
    print()

    # display most commonly used end station and the number of occurrences for this station
    common_end_station = end_station.mode()[0]
    end_station_count = 0
    for station in end_station:
        if station == common_end_station:
            end_station_count += 1

    print('The most popular end station is {}. \nThis station was used {} times.'.format(common_end_station, end_station_count))
    print()

    # display most frequent combination of start station and end station trip and the number of occurrences for this combination
    df['Station Combination'] = start_station +" AND "+ end_station
    common_combo = df['Station Combination'].mode()[0]
    common_station_count = 0
    for station in df['Station Combination']:
        if station == common_combo:
            common_station_count += 1

    print('The most commonly used combination of stations are {}. \nThis combination of stations was used {} times.'.format(common_combo, common_station_count))
    print()

    # display the amount of time it took to run statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print()
    print()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("The total travel time taken by all users (in minutes) is {}".format(total_travel))
    print()

    # display mean travel time
    mean_travel = int(df['Trip Duration'].mean())
    print("The average number of minutes traveled per user is {}.".format(mean_travel))
    print()

    # display the amount of time it took to run statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print()
    print()

    # Display counts of user types
    count_subscriber = 0
    count_customer = 0
    count_unclassified = 0
    for user in df['User Type']:
        if user == 'Customer':
            count_customer += 1
        elif user == 'Subscriber':
            count_subscriber += 1
        else:
            count_unclassified += 1


    print('The total number of subscribers is {}.'.format(count_subscriber))
    print()
    print('The total number of customers is {}.'.format(count_customer))
    print()
    print('The number of unclassified user types is {}.'.format(count_unclassified))
    print()

    # Display counts of gender
    try:
        female_count = 0
        male_count = 0
        no_gender = 0
        for g in df['Gender']:
            if g == 'Female':
                female_count += 1
            elif g == 'Male':
                male_count += 1
            else:
                no_gender += 1
        print('The total number of female users is {}.'.format(female_count))
        print()
        print('The total number of male users is {}.'.format(male_count))
        print()
        print('The total number of users with no gender specified is {}.'.format(no_gender))
        print()
    except:
        print('Sorry, there are no gender statistics for the city of Washington.')
        print()




    # Display earliest, most recent, and most common year of birth
    try:
        current_year = datetime.now().year


        #earliest year
        earliest = int(df['Birth Year'].min())

        #calculates the number of earliest birth year occurrences
        early_count = 0
        for year in df['Birth Year']:
            if year == earliest:
                early_count += 1

        #calculates the age of the earliest birth year user
        earliest_age = current_year - earliest

        print('The earliest year a user was born is {}. \nToday, these users would be {} year old! \nIt looks like {} bikeshare users were born in {}.'.format(earliest, earliest_age, early_count, earliest))
        print()

        #most recent year
        recent = int(df['Birth Year'].max())

        #calculates the number of most recent birth year occurrences
        recent_count = 0
        for year in df['Birth Year']:
            if year == recent:
                recent_count += 1

        #calculates the age of the most recent birth year user
        recent_age = current_year - recent

        print('The most recent year a user was born is {}. \nToday, these users would be {} years old! \nIt looks like {} bikeshare users were born in {}.'.format(recent, recent_age, recent_count, recent))
        print()

        #most common year
        common_year = int(df['Birth Year'].mode()[0])

        #calculates the number of most common birth year occurrences
        common_number = 0
        for year in df['Birth Year']:
            if year == common_year:
                common_number += 1

        #calculates the age of the common birth year user
        common_age = current_year - common_year

        print('The most common year a user was born is {}. \nToday, these users would be {} years old! \nIt looks like {} bikeshare users were born in {}.'.format(common_year, common_age, common_number, common_year))
        print()
    except:
        print('Sorry, there are no birth year statistics for the city of Washington.')
        print()



    # display the amount of time it took to run statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display 5 rows of raw data
        df_raw = pd.read_csv(CITY_DATA[city])
        start_row_num = 0
        end_row_num = 5
        while True:
            see_raw = input('\nDo you want to see 5 lines of raw bike share user data? You\'ll get to see all the stats in a fun chart! Enter yes or no.\n')
            print()
            if see_raw.lower() != 'no':
                print(df_raw[start_row_num:end_row_num])
                start_row_num += 5
                end_row_num += 5
            else:
                break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
