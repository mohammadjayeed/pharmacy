from rest_framework.throttling import AnonRateThrottle

class ProductDetailViewThrottle(AnonRateThrottle):
    scope = 'prod_detail'

class TotalAnonVisit(AnonRateThrottle):
    scope = 'custom'