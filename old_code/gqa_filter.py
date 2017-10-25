from __future__ import absolute_import, division, print_function
"""
Some functions to filter datasets based on their attached GQA.

This functions probably shouldn't be used any more, since support for 
this sort of filtering is now built into the ``datacube.index`` code
and can be performed in the Database, instead of in Python land.
"""
import math

from datacube.utils import intersects
from datacube.api.query import Query, query_group_by


def get_gqa(index, id_):
    dataset = index.datasets.get(id_, include_sources=True)
    mean_dic = dataset.sources['0'].sources['level1'].metadata_doc['gqa']['residual']['iterative_mean']
    mean_sq_val = math.hypot(mean_dic['x'], mean_dic['y'])
    return mean_sq_val


def list_gqa_filtered_cells(index, gw, pix_th=1, cell_index=None, **indexers):
    geobox = gw.grid_spec.tile_geobox(cell_index)
    query = Query(index=index, **indexers)
    observations = index.datasets.search_eager(**query.search_terms)
    # filter now with pixel threshold value
    datasets = {}
    for dataset in observations:
        if intersects(geobox.extent, dataset.extent.to_crs(gw.grid_spec.crs)):
            if get_gqa(index, dataset.id) < pix_th:
                datasets.setdefault(cell_index, {'datasets': [],
                                                 '_geobox': geobox})['datasets'].append(dataset)
    return gw.group_into_cells(datasets, query_group_by(**indexers))
