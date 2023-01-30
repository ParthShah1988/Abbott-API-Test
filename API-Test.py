import requests
import numpy as np
import json

baseURL = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"
response = requests.get(baseURL)

# ------Point to the node in json response----------
response_dict = response.json()
# print("This is response dict->", response_dict.get('data')[0]['Year'])

data = json.loads(response.text)
# print(data)
# print("This is response json load->", data.get('annotations'))

# -------Displaying the response in structure format of Key: value pair-------
#for key, value in data.items():
    #print(f"{key}: {value}")

# --------Validating the response code-----------------
if response.status_code != 200:
    raise ValueError("Error: status code is: " + str(response.status_code))

# -------Storing the source name from the API---------
source = response_dict.get('source')[0]['annotations']['source_name']

# Logic to get the total count of years the API has
populationCount = []
yearCount = []
totalYears = 0

for year in data['data']:
    totalYears = totalYears + 1
    # print(year['Year'], year['Population'])
    # print("The count is", totalYears)
    populationCount.append(year['Population'])
    yearCount.append((year['Year']))
    # print(yearCount)
    # a = year['Population']

# print("This is populationCount: ", populationCount)
# print("This is yearCount: ", yearCount)

# reversing the populationCount array
populationCount.reverse()
#print("This is populationCount 2013 to 2020: ", populationCount)
yearCount.reverse()
#print("This is yearCount 2013 to 2020: ", yearCount)

# print(np.min(yearCount)) --- This is giving error

# Logic to get the minimum and maximum year from the API
maxYear = (response_dict.get('data')[0]['Year'])
minYear = (response_dict.get('data')[totalYears - 1]['Year'])
# print(maxYear)
# print(minYear)

# -------Logic to get the peak growth % of population and its year from the API---------
len_populationCount = len(populationCount)
percentageOfPopulation = []
c = 1
for c in range(len_populationCount):
    percentageOfPopulation.append((populationCount[c] - populationCount[c - 1]) / populationCount[c] * 100)
    c = c + 1
    # print("The value of c: ", c)
    # print(percentageOfPopulation)

percentageOfPopulation.pop(0)  # pop of the 1st index value as per logic
# print("Final list of % of population: ", percentageOfPopulation)

# ----------Population growth % min and max-------------
peakPopulationGrowth = np.max(percentageOfPopulation)
lowestPopulationGrowth = np.min(percentageOfPopulation)

# print("This is the peak % growth in population: ", peakPopulationGrowth)
# print("This is the lowest % growth in population: ", lowestPopulationGrowth)

# -----Index value of peak percentage population growth values---------
# print(percentageOfPopulation.index(peakPopulationGrowth) + 1)
# print(percentageOfPopulation.index(lowestPopulationGrowth) + 1)

# -----Year via index value of peak percentage population growth values---------
peakYearGrowth = yearCount[percentageOfPopulation.index(peakPopulationGrowth) + 1]
# print("This is the year with peak growth in population: ", peakYearGrowth)
lowestYearGrowth = yearCount[percentageOfPopulation.index(lowestPopulationGrowth) + 1]
# print("This is the year with lowest growth in population: ", lowestYearGrowth)

# Rounding of the peak dnd lowest population growth to 2 decimals
peakPopulationGrowth = round(peakPopulationGrowth, 2)
lowestPopulationGrowth = round(lowestPopulationGrowth, 2)
# ---------------Main output---------------------
print("According to", source,
      ", in", totalYears, "years from", minYear, "to", maxYear,
      "peak population growth was ", peakPopulationGrowth, "% in", peakYearGrowth,
      " and lowest population increase was", lowestPopulationGrowth, "% in", lowestYearGrowth)