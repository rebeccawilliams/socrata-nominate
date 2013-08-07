Suggest that analytics opened on Socrata portals.

## Check for the portals with analytics already

    ./has_analytics.sh

## Nominate the analytics

### Settings
Specify your credentials.

```sh
export SOCRATA_EMAIL=tom@example.com
export SOCRATA_PASSWORD=hmkmovq223h89u,hr9on
```

### Run
Request the a dataset from all of the sites without an analytics page.

```sh
phantomjs socrata.js [title] [description] [attachment]
```

### Limitations
This tool doesn't support the attachment field.
