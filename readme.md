Suggest that datasets be opened on Socrata portals.

## Install
This library might expand to other Socrata methods,
so I just named it `socrata`.

    pip install socrata

## Settings
Specify your credentials.

    SOCRATA_EMAIL=tom@example.com
    SOCRATA_PASSWORD=hmkmovq223h89u,hr9on

## Command-line interface
Specify the title and description of the dataset.

    TITLE='Top Ten Elevator Offenders'
    DESCRIPTION='I would like dataset with the addresses of the ten buildings with the most offensive elevators.'

If you would like to nominate the dataset for only one portal,
set the portal.

    PORTAL=nmfs.socrata.com

If you don't specify the portal, the dataset will be nominated
from all of the portals listed on the Socrata [status page](https://status.socrata.com).

## Python interface
Request a dataset for one portal like so.

```python
import socrata
socrata.nominate(
    'nmfs.socrata.com',
    'Top Ten Elevator Offenders',
    'I would like dataset with the addresses of the ten buildings with the most offensive elevators.'
)
```

If you would like to run this on all of the portals,
get the list of sites.

```python
for site in socrata.sites():
    socrata.nominate(
        site, 
        'Top Ten Elevator Offenders',
        'I would like dataset with the addresses of the ten buildings with the most offensive elevators.'
    )
```

## Limitations
This tool doesn't support the attachment field.
