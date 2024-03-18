## collective Astro Index

<br>

#### 👉🏼 quick and dirty proof-of-concept to calculate a collective financial bullish/bearish index, using several western astrological features.

<br>

### tl; dr

* in this package, we build a "collective astrological index" using several collective transit features
* we leverage data from the [astrology api](https://astrologyapi.com/docs/api-ref) (with wrappers inside `src/datalake`) 
* the intel files for the features are located inside `strategies/` and parsed in the files located inside `src/intel/`
* the CLI can be used to inspect the several endpoints and plot the data.
* this is a work in progress.

<br>

---

### installing

<br>

* create a virtualenv and install dependencies:

```bash
virtualen venv
source venv/bin/activate
make install_deps
```

* create an `.env` and add info and API keys:

```bash
cp .env_example .env
vim .env
```

* install:

```bash
make install
```
  
<br>


---

### CLI tool

#### `transit_daily`

<br>

```bash
> astro1 -a

✨ Index I.a: 366.538
```

<br>

#### `transit_monthly`

<br>

```bash
> astro1 -b

✨ Index I.b: {'2023-10-01': 14.97, '2023-10-03': 4.79, '2023-10-06': 4.905, '2023-10-10': 12.883, '2023-10-13': 19.36, '2023-10-18': 19.7, '2023-10-20': 0.0, '2023-10-22': 9.43, '2023-10-24': 29.07, '2023-10-27': 19.6, '2023-10-28': 4.89, '2023-10-31': 12.987}
```

<br>

#### `transit_natal_daily`

<br>

```bash
> astro1 -c

✨ Index I.c: 461.0
```

<br>

#### `moon_phase`

<br>

```bash
> astro1 -d

✨ Index I.d: 0.0
```

<br>

#### `planet_tropical`

<br>

```bash
> astro1 -e

Index I.e: 51.0
```

#### `chart_data`

<br>

```bash
> astro1 -f

✨ Index I.f: 315.428
```

<br>

#### `western_horoscope`

<br>

```bash
> astro1 -g

 Index I.g: 246.01800000000003
```

<br>

#### `natal_wheel`

<br>

```bash
> astro1 -nw

✨ Chart created: https://s3.ap-south-1.amazonaws.com/western-chart/6f3f7540-72de-11ee-a678-d7c61e7f785f.svg
```

<br>

#### `collective_index`


<br>

```bash
> astro1 -ci

 Collective index: {'2023-10-24': 246.69800000000006, '2023-10-01': 14.985, '2023-10-04': 4.9399999999999995, '2023-10-08': 4.985, '2023-10-10': 12.896, '2023-10-13': 19.36, '2023-10-18': 19.68, '2023-10-20': 0.0, '2023-10-22': 9.42, '2023-10-27': 19.6, '2023-10-28': 4.865, '2023-10-30': 4.61, '2023-10-31': 12.948, '2023-10-25': 0.0}
```

<br>


---

### intel files

<br>


#### `rankings.yaml`

<br>

```yaml
# Ranking used to calculate the astro index, which is
# used to determine the overall market sentiment.
# These values are experimental and not normalized.

translation:
  A: 10
  B: 5
  C: 3
  D: 1
  E: 0
  F: -1
  G: -3
  H: -5
  I: -10

sentiments:
  super_bullish: A
  very_bullish: B
  bullish: C
  slightly_bullish: D
  neutral: E
  slightly_bearish: F
  bearish: G
  very_bearish: H
  super_bearish: I

```

<br>


#### `collective.yaml`


<br>

```yaml
# this is a list of all the strategies that are used in the collective strategy
# they are generally used to determine the overall market sentiment
# and they are a high level intel of transits


######################
#     HOUSES
######################

ascendant:
  aries: slightly_bullish        # 5th house leo, 8th house scorpio
  taurus: slightly_bullish       # 5th house virgo, 8th house sagittarius
  gemini: neutral                # 5th house libra, 8th house capricorn
  cancer: slightly_bullish       # 5th house scorpio, 8th house aquarius
  leo: neutral                   # 5th house sagittarius, 8th house pisces
  virgo: neutral                 # 5th house capricorn, 8th house aries
  libra: neutral                 # 5th house aquarius, 8th house taurus
  scorpio: slightly_bearish      # 5th house pisces, 8th house gemini
  sagittarius: neutral           # 5th house aries, 8th house cancer
  capricorn: neutral             # 5th house taurus, 8th house leo
  aquarius: slightly_bullish     # 5th house gemini, 8th house virgo
  pisces: slightly_bearish       # 5th house cancer, 8th house libra


midheaven:
  aries: neutral                 
  taurus: neutral                
  gemini: neutral               
  cancer: neutral                
  leo: neutral                   
  virgo: neutral                 
  libra: neutral                 
  scorpio: neutral               
  sagittarius: neutral           
  capricorn: neutral             
  aquarius: neutral              
  pisces: neutral                


houses:
  1: neutral
  2: slightly_bullish
  3: neutral
  4: neutral
  5: super_bullish
  6: slightly_bearish
  7: neutral
  8: super_bullish
  9: slightly_bullish
  10: slightly_bullish
  11: slightly_bullish
  12: slightly_bearish



######################
#     PLANETS
######################

planets:
  ascendant: neutral
  sun: neutral
  moon: neutral
  mercury: neutral
  venus: super_bullish
  mars: super_bearish
  jupiter: super_bullish
  saturn: super_bearish
  uranus: neutral
  neptune: neutral
  pluto: neutral
  rahu: super_bullish
  ketu: super_bearish
  lilith: neutral
  chiron: neutral


retrograde:
  true: slightly_bullish   
  false: very_bearish            


dignities:
  exalted: super_bullish
  detriment: super_bearish
  fall: super_bearish
  triplicity: neutral
  term: neutral
  face: neutral
  peregrine: neutral

vertex:
  aries: neutral
  taurus: neutral
  gemini: neutral
  cancer: neutral
  leo: neutral
  virgo: neutral
  libra: neutral
  scorpio: neutral
  sagittarius: neutral
  capricorn: neutral
  aquarius: neutral
  pisces: neutral


######################
#     ASPECTS
######################

aspects:
  conjunction: super_bullish
  opposition: super_bearish
  trine: very_bullish
  square: very_bearish
  sextile: bullish
  quincunx: neutral
  semisextile: neutral
  semisquare: neutral
  sesquiquadrate: neutral
  quintile: neutral


######################
#     MOON
######################

moon_phase:
  'first quarter moon': bullish
  'full moon': bearish
  'last quarter moon': neutral
  'new moon': bullish
  'waning crescent moon': neutral
  'waning gibbous moon': neutral
  'waxing crescent moon': neutral
  'waxing gibbous moon': neutral
```

<br>

#### `general.yaml`

<br>

```yaml
# this is a overall list of features that are used so that we
# can define specific strategies in the next yaml files


dignities:
  'sun': 
    'aries': 'exalted'
    'leo': 'domicile'
    'libra': 'detriment'
    'aquarius': 'fall'
  'moon':
    'taurus': 'exalted'
    'cancer': 'domicile'
    'scorpio': 'detriment'
    'capricorn': 'fall'
  'mercury':
    'virgo': 'exalted'
    'gemini': 'domicile'
    'sagittarius': 'detriment'
    'pisces': 'fall'
  'venus':
    'pisces': 'exalted'
    'taurus': 'domicile'
    'scorpio': 'detriment'
    'virgo': 'fall'
  'mars':
    'capricorn': 'exalted'
    'aries': 'domicile'
    'libra': 'detriment'
    'cancer': 'fall'
  'jupiter':
    'cancer': 'exalted'
    'sagittarius': 'domicile'
    'capricorn': 'detriment'
    'gemini': 'fall'
  'saturn':
    'libra': 'exalted'
    'aquarius': 'domicile'
    'aries': 'detriment'
    'cancer': 'fall'
  'uranus':
    'scorpio': 'exalted'
    'aquarius': 'domicile'
    'leo': 'detriment'
    'taurus': 'fall'
  'neptune':
    'pisces': 'exalted'
    'aquarius': 'domicile'
    'virgo': 'detriment'
    'gemini': 'fall'
  'pluto':
    'scorpio': 'exalted'
    'pisces': 'domicile'
    'taurus': 'detriment'
    'virgo': 'fall'
  'rahu':
    'gemini': 'exalted'
  'ketu':
    'sagittarius': 'exalted'
  'north node':
    'gemini': 'exalted'
  'node':
    'gemini': 'exalted'
  'south node':
    'sagittarius': 'exalted'
  'part of fortune':
    'gemini': 'exalted'
  'chiron':
    'virgo': 'domicle'
    'saturn': 'exalted'
  lilith:
    'virgo': 'exalted'
    'capricorn': 'domicile'
    'cancer': 'detriment'
    'taurus': 'fall'

houses_by_element:
  1: 'fire'
  2: 'earth'
  3: 'air'
  4: 'water'
  5: 'fire'
  6: 'earth'
  7: 'air'
  8: 'water'
  10: 'earth'
  11: 'air'
  12: 'water'


signs_by_element:
  'aries': fire
  'taurus': earth
  'gemini': air
  'cancer': water
  'leo': fire
  'virgo': earth
  'libra': air
  'scorpio': water
  'sagittarius': fire
  'capricorn': earth
  'aquarius': air
  'pisces': water


houses_by_sign:
  1: 'aries'
  2: 'taurus'
  3: 'gemini'
  4: 'cancer'
  5: 'leo'
  6: 'virgo'
  7: 'libra'
  8: 'scorpio'
  9: 'sagittarius'
  10: 'capricorn'
  11: 'aquarius'
  12: 'pisces'


aspects:
  'conjunction': 0
  'opposition': 180
  'trine': 120
  'square': 90
  'sextile': 60
  'quincunx': 150
  'semisextile': 30
  'semisquare': 45
  'quintile': 72
  'sesquiquadrate': 135
  'biquintile': 144
  'semisquare': 45
  'novile': 40
  'binovile': 80
  'triseptile': 154
  'quintile': 72
  'septile': 51.42857142857143
  'biseptile': 102.85714285714286
  'triseptile': 154.28571428571428


dignities_by_angles:
  'sun':
    - 19: 'exalted'
  'moon':
    - 3: 'exalted'
  'mercury':
    - 15: 'exalted'
  'venus':
    - 27: 'exalted'
  'mars':
    - 28: 'exalted'
  'jupiter':
    - 15: 'exalted'
  'saturn':
    - 21: 'exalted'
  'rahu':
    - 3: 'exalted'

```



<br>

#### `planet_aspects.yaml`

<br>

```yaml
# this is a list of possible aspects that are used in the strategies
# classified by bullish and bearish indexes in non_normalized_ranking.yaml


moon:
  'conjunction':
      'sun': unclear
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'opposition':
      'sun': unclear
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'trine':
      'sun': unclear
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'square':
      'sun': unclear
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'sextile':
      'sun': unclear
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'semi sextile':
      'sun': unclear
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'quintile':
      'sun': unclear
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'semi square':
      'sun': unclear
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'quincunx':
      'sun': unclear
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear

sun:
  'conjunction': 
    'mercury': unclear
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'opposition':
    'mercury': unclear
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'trine':
    'mercury': unclear
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'square':
    'mercury': unclear
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'sextile':
    'mercury': unclear
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'semi sextile':
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'quintile':
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'semi square':
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'quincunx':
      'mercury': unclear
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear


mercury:
  'conjunction':
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'opposition':
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'trine':
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'square':
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'sextile':
    'venus': unclear
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'semi sextile':
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'quintile':
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'semi square':
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'quincunx':
      'venus': unclear
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear

venus:
  'conjunction':
    'mars': unclear
    'jupiter': super_bullish
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'opposition':
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'trine':
    'mars': unclear
    'jupiter': super_bullish
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'square':
    'mars': unclear
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'sextile':
    'mars': unclear
    'jupiter': bullish
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'semi sextile':
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'quintile':
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'semi square':
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'quincunx':
      'mars': unclear
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear


mars:
  'conjunction': 
    'jupiter': unclear
    'saturn': unclear
    'neptune': unclear
    'pluto': unclear
  'opposition': 
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'trine':
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'square':
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'sextile':
    'jupiter': unclear
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'semi sextile':
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'quintile':
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'semi square':
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'quincunx':
      'jupiter': unclear
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear  


jupiter:
 'conjunction':
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'opposition':
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'trine':
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'square':
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'sextile':
    'saturn': unclear
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
   'semi sextile':
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'quintile':
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'semi square':
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'quincunx':
      'saturn': unclear
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear 

saturn:
  'conjunction':
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'semi sextile':
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'quintile':
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'semi square':
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
    'quincunx':
      'uranus': unclear
      'neptune': unclear
      'pluto': unclear
  'opposition':
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'trine':
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'square':
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  'sextile':
    'uranus': unclear
    'neptune': unclear
    'pluto': unclear
  
uranus:
  'conjunction':
    'neptune': unclear
    'pluto': unclear
  'opposition':
    'neptune': unclear
    'pluto': unclear
  'trine':
    'neptune': unclear
    'pluto': unclear
  'square':
    'neptune': unclear
    'pluto': unclear
  'sextile':
    'neptune': unclear
    'pluto': unclear
  'semi sextile':
      'neptune': unclear
      'pluto': unclear
  'quintile':
      'neptune': unclear
      'pluto': unclear
    'semi square':
      'neptune': unclear
      'pluto': unclear
    'quincunx':
      'neptune': unclear
      'pluto': unclear
  
neptune:
  'conjunction':
    'pluto': unclear
  'opposition':
    'pluto': unclear
  'trine':
    'pluto': unclear
  'square':
    'pluto': unclear
  'sextile':
    'pluto': unclear
  'semi sextile':
      'pluto': unclear
  'quintile':
      'pluto': unclear
    'semi square':
      'pluto': unclear
    'quincunx':
      'pluto': unclear
```
