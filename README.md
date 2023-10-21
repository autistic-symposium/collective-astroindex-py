## astroindex

<br>


## install

<br>

* create a virtualenv, add data to `.env`, and run `make install`
* strategies and intels are located at `strategies/`
  
<br>

### collective index


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


<br>



### todo


* [move out from setup.py](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html), fix makefile, etc.
* unit tests

