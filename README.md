## astroindex

<br>

TODO: clean up this README

https://astrologyapi.com/docs/api-ref

<br>

## install

<br>

* create a virtualenv, add data to `.env`, and run `make install`
* strategies and intels are located at `strategies/`
  
<br>

### collective index

![Screenshot 2023-10-21 at 10 05 41 PM](https://github.com/choices-game/astroindex-py/assets/1130416/131c7deb-94b2-4152-bd68-3af53b09af8d)

<br>

```bash
> choices -cn

🟨 No city or country provided. Using current location.
Starting new HTTP connection (1): ipinfo.io:80
http://ipinfo.io:80 "GET /json HTTP/1.1" 200 None
Requested http://ipinfo.io/json
🟨 Using coordinates 34.1121, -118.2594
🟨 Using timezone -7.0
🟨 Using timezone America/Los_Angeles
🟨 Current time is 2023-10-20 23:21:42.689499-07:00
🟨 Using date 20/10/2023 23:21
🟨 Requesting URL https://json.astrologyapi.com/v1/tropical_transits/daily
Starting new HTTPS connection (1): json.astrologyapi.com:443
https://json.astrologyapi.com:443 "POST /v1/tropical_transits/daily?header=Content-Type%3A+application%2Fjson HTTP/1.1" 200 None
🟨 Ascendant now: cancer
🟨 Signs of planets now: {'sun': 'libra', 'moon': 'capricorn', 'mercury': 'libra', 'venus': 'virgo', 'mars': 'scorpio', 'jupiter': 'taurus', 'saturn': 'pisces', 'uranus': 'taurus', 'neptune': 'pisces', 'pluto': 'capricorn'}
🟨 Planets in houses now: {1: [], 2: [], 3: ['venus'], 4: ['sun', 'mercury'], 5: ['mars'], 6: [], 7: ['moon', 'pluto'], 8: [], 9: ['saturn', 'neptune'], 10: [], 11: ['jupiter', 'uranus'], 12: []}
🟨 Retrogrades now: ['jupiter', 'saturn', 'uranus', 'neptune']
🟨 jupiter is retrograde
🟨 saturn is retrograde
🟨 mars is in house 5
🟨 Collective index updated to: -9
```


<p align="center">
<img src="https://github.com/choices-game/astroindex-py/blob/main/docs/collective_transit_index_october_2023.png" width="80%" align="center" style="padding:1px;border:1px solid black;"/>
</p>






<br>



### todo


* [move out from setup.py](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html), fix makefile, etc.
* unit tests
* save date data
* add path of fortune and others
* fix general
* add progressed charts
* add temporal line for index over time (every 2 hours when the ascendant changes)
* add eclipse
* plot things with numpy, etc.
* fix readme with examples
* create an api
    * dockerize
* add support to other aspects
* add linter
* backtest results on real data
* add retrogrades and shadows
* forecast with moon
* do natal chart
    - do natal_transits daily and weekly
* do token chart
    - synatry with token chart
* finish complete aspects.yaml
* research llama and all
* normalize and tune the indexes
* find a better moon api
    - https://www.worldweatheronline.com/weather-api/api/astronomy-api.aspx
    - https://www.aerisweather.com/support/docs/api/reference/endpoints/sunmoon-moonphases/
    - https://www.meteomatics.com/en/api/available-parameters/moon/#moon_phase
* set postman
* check
    https://www.astrolog.org/ftp/astrolog.htm, https://github.com/CruiserOne/Astrolog
* understand tripicities
    - https://www.skyscript.co.uk/triplicities.html
* check intel
    - https://skyscript.co.uk/wealthelect.html
* taurus moon is exalted at 3 degrees
* moon void of course
* at some point we can build our own api, so we don't need to rely on an external api
* rename collective to "astrology api" or something, and remove intel from it
* normalize the data
* check enigma https://radixpro.com/enigma/ 
* check https://mirror.xyz/polymarket.eth 
* check https://uma.xyz/#osnap 
* check astronomy https://docs.astronomyapi.com/
* check https://github.com/astrorigin/pyswisseph 
* astrologer studies https://www.astrologer.com/studies 
* graphs from https://cafeastrology.com/businessromancegraphs.html 


