Suggest that datasets be opened on Socrata portals.

## Install
This library might expand to other Socrata methods,
so I just named it `socrata`.

```sh
pip install socrata
```

## Settings
Specify your credentials.

```sh
export SOCRATA_EMAIL=tom@example.com
export SOCRATA_PASSWORD=hmkmovq223h89u,hr9on
```

## Nominating a dataset
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
