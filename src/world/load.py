import os
from django.contrib.gis.utils import LayerMapping
from world.models import WorldBorder, world_mapping

world_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'TM_WORLD_BORDERS-0.3.shp'))

def run(verbose=True):
    lm = LayerMapping(WorldBorder, world_shp, world_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)
