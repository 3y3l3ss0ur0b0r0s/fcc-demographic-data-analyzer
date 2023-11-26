import pandas as pd


def calculate_demographic_data(print_data=True):
  try:
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    # age,workclass,fnlwgt,education,education-num,marital-status,occupation,relationship,race,sex,capital-gain,capital-loss,hours-per-week,native-country,salary
  
  except:
    raise Exception('Could not read CSV.')
    
  else:
    # Print df for reference/testing...
    print(df)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts(ascending=False)

    # What is the average age of men?
    average_age_men = round(df.loc[df['sex'] == 'Male']['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    bachelors_df = df.loc[df['education'] == 'Bachelors']
    #non_na = df.dropna(subset='education')
    percentage_bachelors = round(((len(bachelors_df) / len(df)) * 100), 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    higher_df = df.loc[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    higher_rich_df = higher_df.loc[df['salary'] == '>50K']
    
    # What percentage of people without advanced education make more than 50K?
    lower_df = df.loc[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_rich_df = lower_df.loc[df['salary'] == '>50K']

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = (round(len(higher_df) / len(df), 1)) * 100
    lower_education = (round(len(lower_df) / len(df), 1)) * 100

    # percentage with salary >50K
    higher_education_rich = round(((len(higher_rich_df) / len(higher_df)) * 100), 1)
    lower_education_rich = round(((len(lower_rich_df) / len(lower_df)) * 100), 1) 
    
    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_workers_df = df.loc[df['hours-per-week'] == min_work_hours]
    num_min_workers = len(min_workers_df)
    num_rich_min_workers = len(min_workers_df.loc[min_workers_df['salary'] == '>50K'])
      
    rich_percentage = round(((num_rich_min_workers / num_min_workers) * 100), 1)

    # What country has the highest percentage of people that earn >50K?
      # Get total of people in each country with a high salary
    country_high_salaries_df = df.loc[df['salary'] == '>50K'].groupby(['native-country', 'salary']).size().reset_index(name='counts')

      # Get total of people in each country
    country_all_salaries_df = df.groupby(['native-country']).size().reset_index(name='counts')

      # Get percentage of high salary earners in each country
    joined_df = country_high_salaries_df.join(country_all_salaries_df.set_index('native-country'), lsuffix='_high', rsuffix='_all', on='native-country')
    joined_df['percentage'] = joined_df.apply(lambda x : round((x['counts_high'] / x['counts_all']) * 100, 1), axis=1)
    joined_df.set_index('native-country', inplace=True)
    
    highest_earning_country = joined_df['percentage'].idxmax()
    highest_earning_country_percentage = joined_df.loc[highest_earning_country]['percentage']

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df.loc[df['native-country'] == 'India']['occupation'].mode()[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
