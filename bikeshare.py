import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington)
    city = input('Which city would you like to analyze? (chicago, new york city, washington): ').lower()
    while city not in CITY_DATA:
        city = input('Invalid city. Please enter a valid city: ').lower()
    # Get user input for month (all, january, february, ... , june)
    month = input('Which month would you like to filter by? (all, january, february, ... , june): ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Invalid month. Please enter a valid month: ').lower()
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week would you like to filter by? (all, monday, tuesday, ... sunday): ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Invalid day. Please enter a valid day: ').lower()
    print('-'*40)
    return city, month, day


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
   """
   Loads data for the specified city and filters by month and day if applicable.
   Args:
       city (str): The name of the city to analyze.
       month (str): The name of the month to filter by, or "all" to apply no month filter.
       day (str): The name of the day of week to filter by, or "all" to apply no day filter.
   Returns:
       A Pandas DataFrame containing city data filtered by month and day.
   """
   # Check if the city argument is valid.
   if city not in CITY_DATA:
       raise ValueError(f"Invalid city: {city}")
   # Check if the month argument is valid.
   if month not in ["all", "january", "february", "march", "april", "may", "june"]:
       raise ValueError(f"Invalid month: {month}")
   # Check if the day argument is valid.
   if day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
       raise ValueError(f"Invalid day: {day}")
   # Load the data for the specified city.
   df = pd.read_csv(CITY_DATA[city])
   # Convert the "Start Time" column to a datetime type.
   df["Start Time"] = pd.to_datetime(df["Start Time"])
   # Filter by month if applicable.
   MONTHS = {
    "january": 1, 
    "february": 2,
     "march": 3,
     "april": 4,
     "may": 5,
     "june": 6,
      }

   if month != "all":
    df = df[df["Start Time"].dt.month == MONTHS[month]]
   # Filter by day of week if applicable.
   if day != "all":
       # Convert the day of the week to an integer.
       day_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(day)
       df = df[df["Start Time"].dt.weekday == day_of_week]
   return df
def time_stats(df):
  """
  Displays statistics on the most frequent times of travel.
  """
  print('\nCalculating The Most Frequent Times of Travel...\n')
  start_time = time.time()
  # Display the most common month
  most_common_month = df['Start Time'].dt.month.mode()[0]
  print('The most common month is:', most_common_month)
  # Display the most common day of week
  most_common_day_of_week = df['Start Time'].dt.day_name().mode()[0]
  print('The most common day of the week is:', most_common_day_of_week)
  # Display the most common start hour
  try:
    result = df['Start Time'].dt.strftime('%H:%M').value_counts()
    most_common_start_hour = result.index[0]
    print('The most common start hour is:', most_common_start_hour)
  except IndexError:
    print('There is no mode for the start hour.')
    # If the `result` Series is empty, use the `median()` method to find the most common start hour.
    most_common_start_hour = df['Start Time'].dt.strftime('%H:%M').median()
    print('The most common start hour is:', most_common_start_hour)
  except Exception as e:
    print('An error occurred while calculating the most common start hour.')
    print(e)
  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)
def station_stats(df):
  """Displays statistics on the most popular stations and trip."""

  print('\nCalculating The Most Popular Stations and Trip...\n')
  start_time = time.time()

  # Display most commonly used start station
  most_common_start_station = df['Start Station'].mode()[0]
  print('The most commonly used start station is:', most_common_start_station)

  # Display most commonly used end station

  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)
    
def trip_duration_stats(df):
  """
  Displays statistics on the total and average trip duration.
  """
  print('\nCalculating Trip Duration...\n')
  start_time = time.time()
  # Display total travel time
  total_travel_time = df['Trip Duration'].sum()
  print('The total travel time is:', total_travel_time, 'seconds.')
  # Display mean travel time
  if not df['Trip Duration'].empty:
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel time is:', mean_travel_time, 'seconds.')
  else:
    print('There is no average travel time')
  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)
def display_data(df, start_loc=0):
  """Displays 5 rows of raw data from the given DataFrame.

  Args:
    df: A Pandas DataFrame.
    start_loc: The row index to start displaying data from.
  """

  # Check if there is any more data to display.
  if start_loc >= len(df):
    return

  # Print the next 5 rows of data.
  print(df.iloc[start_loc:start_loc + 5])

  # Ask the user if they want to continue displaying data.
  view_data = input("Do you wish to continue?: ").lower()
  if view_data == "yes":
    display_data(df, start_loc + 5)    
def user_stats(df):
  """
  Displays statistics on bikeshare users.
  """
  print('\nCalculating User Stats...\n')
  start_time = time.time()
  # Display counts of user types
  if not df['User Type'].empty:
    user_types = df['User Type'].value_counts()
    print('Counts of user types')
    print(user_types)
  else:
    print('There are no user types')
  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)
def main():
  while True:
    try:
      city, month, day = get_filters()
      df = load_data(city, month, day)

      time_stats(df)
      user_stats(df)
      trip_duration_stats(df)

      # Display raw data upon request.
      display_data(df)

      restart = input('\nWould you like to restart? Enter yes or no.\n')
      if restart.lower() != 'yes':
        break
    except Exception as e:
      print(e)
      print('An error occurred while running the program.')


if __name__ == "__main__":
  main()
  try:
    main()
  except Exception as e:
    print(e)
    print('An error occurred while running the program.')
