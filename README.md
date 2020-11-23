# virtual-school-automation
Web scraping, zoom automation, etc
## Installing packages
Install python
Install everything with ```pip install [packagename]```
Run ```scrapeSchoology.py``` as the main code.

The purpose of main.py is to:
* Check constantly for the right time
* If the time is on the spreadsheet, run the right program (either through zoom or my schoology conferences)

ScrapeSchoology does:
* Signs into schoology
* Finds zoom info from my physics teacher's post
* Uses a regular expression to isolate the codes
* Adds the info to a .csv, along with the time, depending on day of the week
* Starts checking for meetings, using functions imported from ```zoomAutomation.py```

ZoomAutomation does:
* Checks every 15 seconds to see if the current time matches a time from ```timings.csv```
* If it's a weekend, it asks if you want to continue
* When it's time, it launches zoom, clicks on Join Meeting, enters the info, and enters the waiting room
