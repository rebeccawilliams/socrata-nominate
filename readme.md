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
Request that the analytics page be opened.

```sh
phantomjs nominate.js
```

This reads the description from `description.txt`.

### Limitations
This tool doesn't support the attachment field.
