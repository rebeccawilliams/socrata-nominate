import nose.tools as n
import socrata._sites as sites

def test_sites():
    n.assert_in('data.cityofnewyork.us', set(sites.sites()))
