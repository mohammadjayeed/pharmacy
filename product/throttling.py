from rest_framework.throttling import AnonRateThrottle


#These two throttle classes restrict anonymous users

#Throttle caches maintain persistent anonymous data in docker containers

class ProductDetailViewThrottle(AnonRateThrottle):

    '''View specific throttle control for anom'''

    scope = 'prod_detail'

class TotalAnonVisit(AnonRateThrottle):

    '''All in all throttle control for anom'''

    scope = 'custom'