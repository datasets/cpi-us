<a className="gh-badge" href="https://datahub.io/core/cpi-us"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Consumer Price Index for *All Urban Consumers (CPI-U)* from U.S. Department
Of Labor Bureau of Labor Statistics. This is a monthly time series from January 1913. Values are U.S. city averages for all items and
1982-84=100. Note that there are many price indices and this is only one of
them (albeit the most standard and with the longest set of data).

## Preparation

Run the following script to get the final data at `data/` folder:
```
# Install libraries
pip install -r scripts?requirements.txt

# Run the script
python scripts/process.py
```

## Data

Data is sourced from [bls.gov](https://api.bls.gov/publicAPI/v2/timeseries/data/) and combined with previous data from 2014 which is now outdated and requires an API for this case.

## Automation
Up-to-date (auto-updates every month) cpi-us dataset could be found on the datahub.io: https://datahub.io/core/cpi-us

## License

This Data Package is made available under the Public Domain Dedication and License v1.0 whose full text can be found at: http://www.opendatacommons.org/licenses/pddl/1.0/
