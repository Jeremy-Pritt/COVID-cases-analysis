import requests
import json
import numpy as np
import datetime

# create a function to get the month name from a number


def getMonth(num):
    if num == 1:
        return "January"
    elif num == 2:
        return "February"
    elif num == 3:
        return "March"
    elif num == 4:
        return "April"
    elif num == 5:
        return "May"
    elif num == 6:
        return "June"
    elif num == 7:
        return "July"
    elif num == 8:
        return "August"
    elif num == 9:
        return "September"
    elif num == 10:
        return "October"
    elif num == 11:
        return "November"
    elif num == 12:
        return "December"
    else:
        return "N/A"


# assign the url and the countries list
covid_api_url = "https://covid-api.mmediagroup.fr/v1/history"
# ADD Russia, US, and something else
countries = ["US", "Russia", "New Zealand"]

# create a loop to perform logic on eachcountry in the country list
for i in range(len(countries)):

    # get the api data
    country_api_data = requests.get(covid_api_url, "country=" + countries[i]
                                    + "&status=confirmed")

    # convert API data to python dictionary
    country_dict = json.loads(country_api_data.text)

    # initialize lists to store dates and confirmed cases
    dates = []
    cases_cumulative = []

    # initialize the start and end date for our data
    start_date = "2020-01-21"
    end_date = "2021-12-31"

    # loop through each of the dates in the dictionary and append data
    # to dates and cases lists; only use data from given date range

    for key, value in country_dict["All"]["dates"].items():
        if key >= start_date and key <= end_date:
            dates.append(key)
            cases_cumulative.append(value)

    # create a reversed cases list to use in the for loop logic
    cases_cumulative_rev = cases_cumulative[::-1]

    # create a for loop to create daily case list, rather than cumulative
    # number of cases
    cases_daily_rev = []
    for i in range(len(cases_cumulative_rev)):
        if i == 0:
            day_cases = 0
            cases_daily_rev.append(day_cases)
        else:
            day_cases = cases_cumulative_rev[i] - cases_cumulative_rev[i-1]
            cases_daily_rev.append(day_cases)

    # reverse the cases_daily_rev so that it is alligned correcty with
    # the dates list
    cases_daily = cases_daily_rev[::-1]

    # pop the last value in the cases_daily list and the dates list
    # this date (2020-01-21) was not meant to be included in our data,
    # but was included in our logic to make sure that we got the correct new daily cases
    cases_daily.pop(-1)
    dates.pop(-1)

    # get the country name
    country_name = country_dict["All"]["country"]

    # get the average number of new daily confirmed cases for the entire set
    avg_daily_cases = round(np.mean(cases_daily), 5)

    # get the date with the highest new number of confirmed cases
    highest_case_date = dates[cases_daily.index(max(cases_daily))]

    # get the most recent date with no confirmed cases
    recent_zero_day = "N/A in Date Range"
    for i in range(len(cases_daily)):
        if cases_daily[i] == 0:
            recent_zero_day = dates[i]
            break

    # create a list of datetimes from the dates list
    datetime_dates = [datetime.datetime.strptime(
        dates[i], "%Y-%m-%d") for i in range(len(dates))]

    # create a list of months and years
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    years = [2020, 2021]

    # create an empty list to hold lists of data by month
    monthly_cases = []

    # loop through each year and month and collect monthly daily cases data
    for year in years:
        for month in months:
            month_dict = {}
            month_list = []
            for i in range(len(datetime_dates)):
                if datetime_dates[i].year == year and datetime_dates[i].month == month:
                    month_list.append(cases_daily[i])
            month_dict["month_year"] = [month, year]
            month_dict["cases"] = month_list
            monthly_cases.append(month_dict)

    # find the month with the most new daily cases by looping through the
    # monthly cases dictionary
    highest_month = ""
    cases_counter = -1
    for month in monthly_cases:
        if sum(month["cases"]) > cases_counter:
            cases_counter = sum(month["cases"])
            highest_month = month["month_year"]

    # call the getMonth function to change the highest_month variable
    # into a string providing the month and year
    highest_month = getMonth(highest_month[0]) + " " + str(highest_month[1])

    # find the month with the least new daily cases by looping through the
    # montly cases dictionary
    lowest_month = ""
    cases_counter = 100000000000
    for month in monthly_cases:
        if sum(month["cases"]) < cases_counter:
            cases_counter = sum(month["cases"])
            lowest_month = month["month_year"]

    # call the getMonth function to change the highest_month variable
    # into a string providing the month and year
    lowest_month = getMonth(lowest_month[0]) + " " + str(lowest_month[1])

    # print the output
    print("Covid confirmed cases statistics")
    print("Country name:", country_name)
    print("Average number of new daily confirmed cases for the entire dataset:", avg_daily_cases)
    print("Date with the highest new number of confirmed cases:", highest_case_date)
    print("Most recent date with no new confirmed cases:", recent_zero_day)
    print("Month with the highest new number of confirmed cases:", highest_month)
    print("Month with the lowest new number of confirmed cases:", lowest_month)
    print()

    # put all the data into a dictionary
    result_dict = {}
    result_dict["Country Name"] = country_name
    result_dict["Average Daily New Cases"] = avg_daily_cases
    result_dict["Highest Case Count Day"] = highest_case_date
    result_dict["Recent Zero Case Day"] = recent_zero_day
    result_dict["Highest New Cases Month"] = highest_month
    result_dict["Lowest New Cases Month"] = lowest_month
    result_dict["Dates"] = dates
    result_dict["Daily Number of New Cases"] = cases_daily

    # save the data into a json file
    with open(result_dict["Country Name"] + ".json", 'w') as fp:
        json.dump(result_dict, fp,  indent=4)
