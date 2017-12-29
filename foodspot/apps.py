from __future__ import unicode_literals
from django.apps import AppConfig


class FoodspotConfig(AppConfig):
    name = 'foodspot'

    def ready(self):
    	# import signals module
    	import signals


