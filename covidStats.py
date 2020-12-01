import requests
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
from datetime import datetime
import numpy as np
import json


today = datetime.today().strftime('%Y-%m-%d')
with open ("lastUpdated.txt", "r") as lastUpdated:
    lastUpdate = lastUpdated.read().strip('\n')

if today != lastUpdate:

    URL = "https://api.covid19api.com/total/dayone/country/south-africa"

    r = requests.get(url=URL)

    data = r.json()

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
    
    with open("lastUpdated.txt", "w") as lastUpdated:
        lastUpdated.write(today)

else:
    with open('data.txt') as json_file:
        data = json.load(json_file)


dateList = []
confirmedList = []
deathList = []
recoveredList = []
deathRateList= []
for dictionary in data:
   date =  np.datetime64(dictionary["Date"][0:10:1])
   confirmed = dictionary["Confirmed"]
   deaths = dictionary["Deaths"]
   recovered = dictionary["Recovered"]
   deathRate = deaths/confirmed * 100
   dateList.append(date)
   confirmedList.append(confirmed)
   deathList.append(deaths)
   recoveredList.append(recovered)
   deathRateList.append(deathRate)
   print(f"Date: {date} Confirmed Cases: {confirmed} Deaths: {deaths} Recovered: {recovered}")

w, h = figaspect(9/16)
fig, ax = plt.subplots(figsize=(w,h))
ax.semilogy(dateList, confirmedList, color='teal')
ax.semilogy(dateList, deathList, color='tomato')
ax.semilogy(dateList, recoveredList,  color='yellowgreen')
ax.semilogy(dateList, deathRateList, color="black")
ax.legend(['Confirmed Cases', 'Deaths', 'Recovered', 'Death Rate for Infected'])
ax.set_title("South Africa Covid Graph")
ax.xaxis.set_label_text("Date")
ax.yaxis.set_label_text("Cases")
ax.grid(True)
fig.savefig("Covid19SA.pdf",dpi=120)