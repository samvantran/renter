from django.db import models

import requests
import xmltodict

from renter.settings import ZWS_ID


class Listing(models.Model):
    zpid = models.IntegerField()
    details_url = models.URLField()
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
    zestimate = models.IntegerField()
    rent_cost = models.IntegerField()
    year_built = models.IntegerField()
    sq_ft = models.IntegerField()
    lot_size = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(decimal_places=1, max_digits=3)
    comp_score = models.DecimalField(decimal_places=1, max_digits=3)

    def get_updated_info(self):
        payload = {'zws-id': ZWS_ID, 'zpid': self.zpid, 'count': 1, 'rentzestimate': 'true'}
        req = requests.get('http://www.zillow.com/webservice/GetDeepComps.htm', params=payload)
        result = xmltodict.parse(req.text)

        primary = result['Comps:comps']['response']['properties']['principal']

        prim_addr = primary['address']
        self.street_address = prim_addr['street']
        self.city = prim_addr['city']
        self.state = prim_addr['state']
        self.zipcode = prim_addr['zipcode']
        self.lat = prim_addr['latitude']
        self.lng = prim_addr['longitude']







