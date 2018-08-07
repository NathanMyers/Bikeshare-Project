import pandas as pd
from datetime import datetime
from datetime import timedelta
import time

# Filenames
# chicago = chicago.csv
# new york = new_york.csv
# washington = washington.csv


def get_city():
    '''

    args:
        none
    returns:
        (str) file for bikeshare city data.
    '''
    city = ''
    while city.lower() not in ['chicago', 'new york', 'washington']:
        city = input('\nWelcome! Let\'s take a look at some bikeshare data!\n'
                     'Would you like to see the data for Chicago, New York, or'
                     ' Washington?\n')
    if city.lower() == 'chicago':
        return 'chicago.csv'
    elif city.lower() == 'new york':
        return 'new_york_city.csv'
    elif city.lower() == 'washington':
        return 'washington.csv'
    else:
        print('That was not a valid input. Please enter Chicago, New York '
              'or Washington.')


def get_time_interval():
    '''Asks for the time period and returns filtered result

    args:
        none
    Returns"
        (str) Time filter for the bikeshare data.
    '''
    time_interval = ''
    while time_interval.lower() not in ['month', 'day', 'none']:
        time_interval = input('The data can be filtered by month, day'
                              ' or not at all.Type none for no time filter.')
        if time_interval.lower() not in ['month', 'day', 'none']:
            print('Please enter a valid input')
    return time_interval


def get_month():
    ''' Asks for month and then returns month.

    args:
        none.
        Returns:
        (tuple) Lower & upper limit of the month bikeshare data.
    '''
    input_month = ''
    month_dict = {'january': 1, 'febuary': 2, 'march': 3, 'april': 4,
                  'may': 5, 'june': 6}
    while input_month.lower() not in month_dict.keys():
        input_month = input('Choose any month between January and June')
        if input_month.lower() not in month_dict.keys():
            print('Sorry that was not a valid in put. Please choose a'
                  'month between January and June')
    month = month_dict[input_month.lower()]
    return ('2017-{}'.format(month), '2017-{}'.format(month + 1))


def get_day():
    '''Asks for a day and returns that day.
    Args:
        none.
    Returns:
        (tuple) upper & lower limit of the day of bikeshare data.
    '''
    current_month = get_month()[0]
    month = int(current_month[5:])
    date_valid = False
    while date_valid == False:
        is_int = False
        day = input('Which day do you need data for Monday - Friday')
        while is_int == False:
            try:
                day = int(day)
                is_int = True
            except ValueError:
                print('Your input is invalid, Please respond with a number')
                day = input('\nWhich day? Please type your response'
                            'as an integer.\n')
        try:
            date_to_start = datetime(2017, month, day)
            date_valid = True
        except ValueError as e:
            print(str(e).capitalize())
        end_date = date_to_start + timedelta(days=1)
        return(str(date_to_start), str(end_date))


def pop_month(df):

    ''' Finds + prints most popular month
    args:
    Returns:
        none
    '''

    months = ['January', 'Febuary', 'March', 'April', 'May', 'June']
    month_index = int(df['start_time'].dt.month.mode())
    pop_month = months[month_index - 1]
    print('The most popular month is {}.'.format(pop_month))


def pop_day(df):
    ''' Finds and prints most popular day of the week
    args:
        bikeshare dataframe
        Returns
            none
    '''
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    day_index = int(df['start_time'].dt.month.mode())
    pop_day = days_of_week[day_index]
    print('The most popular day of week for'
          'start time is {}.'.format(pop_day))


def pop_hour(df):
    ''' Finds and prints most popular start time hour
    args:
        bikeshare dataframe
        Returns:
            none
    '''
    pop_hour = int(df['start_time'].dt.hour.mode())
    if pop_hour == 0:
        am_or_pm = 'am'
        pop_hour_formatted = 12
    elif 1 <= pop_hour < 12:
        am_or_pm = 'am'
        pop_hour_formatted = pop_hour
    elif 13 <= pop_hour < 24:
        am_or_pm = 'pm'
        pop_hour_formatted = pop_hour - 12
    print('The most popular time of day for'
          'the start time is {}{}'.format(pop_hour_formatted, am_or_pm))


def trip_duration(df):
    ''' Finds and prints the total trip duration and average trip duration
    args:
        bikeshare dataframe
        Returns:
            none
    '''
    total_duration = df['trip_duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print('The total trip duration is {} hours, {} minutes and {}'
          ' seconds.'.format(hour, minute, second))
    average_duration = round(df['trip_duration'].mean())
    m, s = divmod(average_duration, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print('The average trip duration is {} hours, {} minutes and {}'
              ' seconds.'.format(h, m, s))
    else:
        print('The average trip duration is {} minutes and {} seconds.'.format(m, s))



def pop_stations(df):
    ''' Finds and prints most popular ending station.
    args:
        bikeshare dataframe
        Returns:
            none
    '''

    pop_start = df['start_station'].mode().to_string(index=False)
    pop_end = df['end_station'].mode().to_string(index=False)
    print('The most popular start station is {}.'.format(pop_start))
    print('The most popular end station is {}.'.format(pop_end))


def pop_destination(df):
    ''' Finds and prints the most destination
    args:
        bikeshare dataframe
        Returns:
            none
    '''

    popular_destination = df['journey'].mode().to_string(index=False)
    # column created from statistics() function
    print('The most popular trip is {}.'.format(popular_destination))


def users(df):
    ''' Finds and prints the most destination
    args:
        bikeshare dataframe
        Returns:
            none
    '''

    subscribers = df.query('user_type ==  "Subscriber"').user_type.count()
    customer = df.query('user_type == "Customer"').user_type.count()
    print('There are {} Subscribers and'
          '{} Customers.'.format(subscribers, customer))


def genders(df):
    ''' Finds and prints counts of gender.
    args:
    bikeshare dataframe
    returns:
        none
    '''
    male_count = df.query('gender == "Male"').gender.count()
    female_count = df.query('gender == "Female"').gender.count()
    print('There are {} male users and'
          '{} female users.'.format(male_count, female_count))


def birth_years(df):
    early = int(df['birth_year'].min())
    late = int(df['birth_year'].max())
    mean = int(df['birth_year'].mode())
    print('The oldest users are born in {}.\nThe'
          'youngest users are born in {}.'
          '\nThe most popular'
          'birth year is {}.'.format(early, late, mean))


def display_data(df):
    '''Displays five lines of data. After displaying five lines,
    ask the user if they would like to see additional lines,
    continues asking until directed.
    Args:
        data frame
    Returns:
        none
    '''

    def valid(display):
        if display.lower() in ['yes', 'no']:
            return True
        else:
            return False
    head = 0
    tail = 5
    valid_input = False
    while valid_input == False:
        display = input('\nWould you like to view individual trip data? '
                        'Type \'yes\' or \'no\'.\n')
        valid_input = valid(display)
        if valid_input == True:
            break
        else:
            print("Sorry, I do not understand your input. Please type 'yes' or"
                  " 'no'.")
    if display.lower() == 'yes':
        # prints every column except the 'journey' column created in statistics()
        print(df[df.columns[0:-1]].iloc[head:tail])
        display_more = ''
        while display_more.lower() != 'no':
            valid_input_2 = False
            while valid_input_2 == False:
                display_more = input('\nWould you like to view more individual'
                                     ' trip data? Type \'yes\' or \'no\'.\n')
                valid_input_2 = valid(display_more)
                if valid_input_2 == True:
                    break
                else:
                    print("Sorry, I do not understand your input. Please type "
                          "'yes' or 'no'.")
            if display_more.lower() == 'yes':
                head += 5
                tail += 5
                print(df[df.columns[0:-1]].iloc[head:tail])
            elif display_more.lower() == 'no':
                break


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and
    time period specified by the user via raw input.
    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()
    print('Loading data...')
    df = pd.read_csv(city, parse_dates=['Start Time', 'End Time'])

    # change all column names to lowercase letters
    #and replace spaces with underscores
    new_labels = []
    for col in df.columns:
        new_labels.append(col.replace(' ', '_').lower())
    df.columns = new_labels

    # increases the column width so that the long strings in the 'journey'
    # column can be displayed fully
    pd.set_option('max_colwidth', 100)

    # creates a 'journey' column that concatenates 'start_station' with
    # 'end_station' for the use popular_trip() function
    df['journey'] = df['start_station'].str.cat(df['end_station'], sep=' to ')

    # Filter by time period (month, day, none)
    time_interval = get_time_interval()
    if time_interval == 'none':
        df_filtered = df
    elif time_interval == 'month' or time_interval == 'day':
        if time_interval == 'month':
            filter_lower, filter_upper = get_month()
        elif time_interval == 'day':
            filter_lower, filter_upper = get_day()
        print('Filtering data...')
        df_filtered = df[(df['start_time'] >= filter_lower) & (df['start_time'] < filter_upper)]
    print('\nCalculating the first statistic...')

    if time_interval == 'none' or time_interval == 'day':
        start_time = time.time()

# What is the most popular month for start time?
        pop_month(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")

    if time_interval == 'none' or time_interval == 'month':
        start_time = time.time()

 # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
        pop_day(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

    # What is the most popular hour of day for start time?
    pop_hour(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    trip_duration(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    pop_stations(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    trip_duration(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    users(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))

    if city == 'chicago.csv' or city == 'new_york_city.csv':
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What are the counts of gender?
        genders(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What are the earliest (i.e. oldest user), most recent (i.e. youngest
        # user), and most popular birth years?
        birth_years(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data(df_filtered)

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    while restart.lower() not in ['yes', 'no']:
        print("Invalid input. Please type 'yes' or 'no'.")
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
    statistics()

