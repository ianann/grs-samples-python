import os
import random
import string
import setup_catalog

from google.api_core.client_options import ClientOptions

from google.cloud.retail_v2 import SearchServiceClient, SearchRequest

project_number = "1038874412926"
endpoint = "retail.googleapis.com"
isolation_filter_key = "INTEGRATION_FILTER_KEY"
title_query = "Nest_Maxi"
visitor_id = "visitor"
test_id = ''.join(random.sample(string.ascii_lowercase, 1))

# [START search_client]
default_catalog = "projects/{0}/locations/global/catalogs/default_catalog/branches/0".format(project_number)
default_search_placement = "projects/1038874412926/locations/global/catalogs/default_catalog/placements/default_search"


def get_search_service_client():
    client_options = ClientOptions(endpoint)
    return SearchServiceClient(client_options=client_options)


# [END search_client]


def build_isolation_filter(test__id: str):
    return 'attributes.{0}: ANY("{1}")'.format(isolation_filter_key, test__id)


# [START search_product_with_textual_facet_restricted_values]
def search_products_textual_facet_restricted_values(query: str, key: str, restricted_values: [str]):
    facet_key = SearchRequest.FacetSpec().FacetKey()
    facet_key.key = key
    facet_key.restricted_values = restricted_values
    facet_spec = SearchRequest.FacetSpec()
    facet_spec.facet_key = facet_key

    search_request = SearchRequest()
    search_request.placement = default_search_placement
    search_request.branch = default_catalog
    search_request.query = query
    search_request.filter = build_isolation_filter(test_id)
    search_request.facet_specs = [facet_spec]
    search_request.visitor_id = visitor_id
    print("---search_request:---")
    print(search_request)

    return get_search_service_client().search(search_request)


# [END search_product_with_textual_facet_restricted_values]


def search():
    setup_catalog.ingest_products(test_id)

    search_response = search_products_textual_facet_restricted_values(title_query, "colorFamily", ["black"])
    print("COLORFAMILY RESTRICTED VALUE FACET")
    print(search_response.facets)
    print("RESTRICTED VALUE FACET SEARCH RESULTS")
    print(search_response.results)

    setup_catalog.delete_products()


search()
