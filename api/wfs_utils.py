import requests
from lxml import etree
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import DCTERMS, RDF
from api.config import *
from os.path import *
import logging


def get_no_of_stratunits():
    url = "http://stratunits.gs.cloud.ga.gov.au/stratunit/ows" \
            "?service=WFS" \
            "&request=GetFeature" \
            "&typeName=stratunit%3AStratigraphicUnit" \
            "&version=1.1.0" \
            "&resultType=hits"

    r = requests.get(url)

    return int(r.text.split("numberOfFeatures=\"", 1)[1].split("\"", 1)[0])


def store_stratunit_index(no_of_stratunits):
    r = requests.get(
        "http://stratunits.gs.cloud.ga.gov.au/stratunit/ows"
        "?service=WFS"
        "&version=1.0.0"
        "&request=GetFeature"
        "&typeName=stratunit%3AStratigraphicUnit"
        "&maxFeatures={}"
        "&propertyname=stratunit:name".format(no_of_stratunits)
    )

    tree = etree.fromstring(r.content)
    features = tree.xpath('//gml:featureMember', namespaces={"gml": "http://www.opengis.net/gml"})
    g = Graph()
    STRAT = Namespace("http://pid.geoscience.gov.au/def/stratunits#")
    GFS = Namespace("http://pid.geoscience.gov.au/geologicFeature/au/")
    g.bind("strat", STRAT)
    g.bind("gfs", GFS)
    g.bind("dcterms", DCTERMS)

    for feature in features:
        fid = "SU" + feature.xpath(
            './/stratunit:StratigraphicUnit/@fid', namespaces={"stratunit": "http://www.ga.gov.au/stratunit"}
        )[0].replace("StratigraphicUnit.", "")
        name = feature.xpath('.//stratunit:name/text()', namespaces={"stratunit": "http://www.ga.gov.au/stratunit"})[0]
        this_feature_uri = GFS[fid]
        g.add((
            this_feature_uri,
            RDF.type,
            STRAT.Unit
        ))
        g.add((
            this_feature_uri,
            DCTERMS.identifier,
            Literal(fid)
        ))
        g.add((
            this_feature_uri,
            DCTERMS.title,
            Literal(name)
        ))

    g.serialize(destination="stratunits-index.ttl", format="turtle")

    print("index stored")


def get_no_of_provinces():
    url = "http://services.ga.gov.au/gis/services/Australian_Geological_Provinces/MapServer/WFSServer" \
          "?service=WFS" \
          "&request=GetFeature" \
          "&version=1.1.0" \
          "&typeName=Australian_Geological_Provinces:AllProvinces" \
          "&resultType=hits"

    r = requests.get(url)
    return int(r.text.split("numberOfFeatures=\"", 1)[1].split("\"", 1)[0])


def cache_provinces_index(no_of_provinces):
    r = requests.get(
        "http://services.ga.gov.au/gis/services/Australian_Geological_Provinces/MapServer/WFSServer?"
        "service=WFS"
        "&request=GetFeature"
        "&version=1.1.0"
        "&typeName=Australian_Geological_Provinces:AllProvinces"
        "&maxFeatures={}"
        "&propertyname=Australian_Geological_Provinces:provinceName".format(no_of_provinces)
    )
    tree = etree.fromstring(r.content)
    features = tree.xpath('//gml:featureMember', namespaces={"gml": "http://www.opengis.net/gml"})
    g = Graph()
    STRAT = Namespace("http://pid.geoscience.gov.au/def/stratunits#")
    GFS = Namespace("http://pid.geoscience.gov.au/geologicFeature/au/")
    g.bind("strat", STRAT)
    g.bind("gfs", GFS)
    g.bind("dcterms", DCTERMS)

    for feature in features:
        fid = "PR" + feature.xpath(
            './/Australian_Geological_Provinces:provinceID/text()',
            namespaces={
                "Australian_Geological_Provinces": "WFS"
            }
        )[0].replace("GA.GeologicProvince.", "")
        name = feature.xpath(
            './/Australian_Geological_Provinces:provinceName/text()',
            namespaces={
                "Australian_Geological_Provinces": "WFS"
            }
        )[0]
        this_feature_uri = GFS[fid]
        g.add((
            this_feature_uri,
            RDF.type,
            STRAT.Province
        ))
        g.add((
            this_feature_uri,
            DCTERMS.isPartOf,
            URIRef("http://example.com/dataset/agp/agp")
        ))
        g.add((
            this_feature_uri,
            DCTERMS.identifier,
            Literal(fid)
        ))
        g.add((
            this_feature_uri,
            DCTERMS.title,
            Literal(name)
        ))

    g.serialize(destination=join(DATA_DIR, "provinces-index.ttl"), format="turtle")

    logging.info("provinces index stored")


def safe_list_get(ls, idx, default):
    try:
        return ls[idx]
    except IndexError:
        return default


def get_province(province_id, return_original_xml=False):
    post_xml = """<GetFeature service="WFS" version="1.1.0"
      outputFormat="GML3"
      xmlns="http://www.opengis.net/wfs"
      xmlns:ogc="http://www.opengis.net/ogc"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:Australian_Geological_Provinces="WFS"
      xsi:schemaLocation="http://www.opengis.net/wfs
                          http://schemas.opengis.net/wfs/1.0.0/WFS-basic.xsd">
      <Query typeName="Australian_Geological_Provinces:AllProvinces">
        <ogc:Filter>
           <ogc:PropertyIsEqualTo>
               <ogc:PropertyName>provinceID</ogc:PropertyName>
              <ogc:Literal>{}</ogc:Literal>
           </ogc:PropertyIsEqualTo>
        </ogc:Filter>
      </Query>
    </GetFeature>
    """.format(province_id)
    headers = {'Content-Type': 'application/xml'}
    r = requests.post(
        "http://services.ga.gov.au/gis/services/Australian_Geological_Provinces/MapServer/WFSServer",
        data=post_xml,
        headers=headers
    )
    if return_original_xml:
        return r.text

    namespaces = {
        "Australian_Geological_Provinces": "WFS",
        "gml": "http://www.opengis.net/gml"
    }
    tree = etree.fromstring(r.content)
    return {
        "title": safe_list_get(tree.xpath('//Australian_Geological_Provinces:provinceName/text()', namespaces=namespaces), 0, None),
        "description": safe_list_get(tree.xpath('//Australian_Geological_Provinces:description/text()', namespaces=namespaces), 0, None),
        "overview": safe_list_get(tree.xpath('//Australian_Geological_Provinces:overview/text()', namespaces=namespaces), 0, None),
        "source": safe_list_get(tree.xpath('//Australian_Geological_Provinces:source/text()', namespaces=namespaces), 0, None),
        "type": safe_list_get(tree.xpath('//Australian_Geological_Provinces:type/text()', namespaces=namespaces), 0, None),
        "older": safe_list_get(tree.xpath('//Australian_Geological_Provinces:representitiveOlderAge_uri/text()', namespaces=namespaces), 0, None),
        "younger": safe_list_get(tree.xpath('//Australian_Geological_Provinces:representitiveYoungerAge_uri/text()', namespaces=namespaces), 0, None),
        "metadata": safe_list_get(tree.xpath('//Australian_Geological_Provinces:metadata_uri/text()', namespaces=namespaces), 0, None),
        "rank": safe_list_get(tree.xpath('//Australian_Geological_Provinces:rank/text()', namespaces=namespaces), 0, None),
        "parent_id": safe_list_get(tree.xpath('//Australian_Geological_Provinces:parentID/text()', namespaces=namespaces), 0, None),
        "parent_name": safe_list_get(tree.xpath('//Australian_Geological_Provinces:parentName/text()', namespaces=namespaces), 0, None),
        "bbox":
            tree.xpath('//gml:lowerCorner/text()', namespaces=namespaces)[0] + " " +
            tree.xpath('//gml:upperCorner/text()', namespaces=namespaces)[0],
        "coords": safe_list_get(tree.xpath('//gml:posList/text()', namespaces=namespaces), 0, None),
    }


def cache_stratigraphic_rank():
    q = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        CONSTRUCT {
            ?c skos:prefLabel ?pl .
        }
        WHERE {
            ?c a skos:Concept ;
               skos:prefLabel ?pl .
        
            <http://resource.geosciml.org/classifier/cgi/stratigraphicrank> skos:member ?c ;
        }
        ORDER BY ?pl
        """
    r = requests.post(
        "http://cgi.vocabs.ga.gov.au/endpoint",
        data={"query": q},
        headers={"Accept": "text/turtle"}
    )

    if not r.ok:
        raise Exception("cache_stratigraphic_rank() failed")
    else:
        with open(join(DATA_DIR, "stratigraphic-rank-concepts.ttl"), "w") as f:
            f.write(r.text)

    logging.info("stratigraphic rank cached")


def cache_timescale_members():
    q = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX gts: <http://resource.geosciml.org/ontology/timescale/gts#>
        CONSTRUCT {
            ?s skos:prefLabel ?pl .
        }
        WHERE { 
          ?s a gts:GeochronologicEra ; skos:prefLabel ?pl .
          FILTER (lang(?pl) = "en")
        } ORDER BY ?pl
        """
    r = requests.post(
        "https://vocabs.ardc.edu.au/repository/api/sparql/"
        "csiro_international-chronostratigraphic-chart_geologic-time-scale-2020",
        data={"query": q},
        headers={"Accept": "text/turtle"}
    )

    if not r.ok:
        raise Exception("cache_timescale_members() failed")
    else:
        with open(join(DATA_DIR, "timescale-members.ttl"), "w") as f:
            f.write(r.text)

    logging.info("timescale members cached")


def cache_geometry_types():
    q = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        CONSTRUCT {
            ?c skos:prefLabel ?pl ;
               skos:notation ?n .
        } 
        WHERE {
          ?c skos:inScheme <http://www.opengis.net/def/isoDataTypes> ;
             skos:prefLabel ?pl ;
             skos:notation ?n .
          
          FILTER REGEX(STR(?c), "^http://www.opengis.net/def/geometry/ISO-19107/2003/")
        }
        ORDER BY ?pl
        """
    r = requests.post(
        "http://defs-dev.opengis.net:8080/rdf4j-server/repositories/ogc-na",
        data={"query": q},
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/turtle"}
    )
    if not r.ok:
        raise Exception("cache_geometry_types() failed")
    else:
        with open(join(DATA_DIR, "iso-19107-geometry-types.ttl"), "w") as f:
            f.write(r.text)

    logging.info("geometry types cached")


if __name__ == "__main__":
    # n = get_no_of_provinces()
    # store_provinces_index(n)
    # # n = get_no_of_stratunits()
    # # store_stratunit_index(n)
    # # get_province("AllProvinces.3")
    # # import pprint
    # # pprint.pprint(get_province("GA.GeologicProvince.1"))

    # print(cache_timescale_types())
    get_province("20368")

    #get_province("20527")


# http://pid.geoscience.gov.au/feature/id/ga/gsmlp/geologicunitview/28

# dataset <http://pid.geoscience.gov.au/dataset/ga/21884>

# Strat Unit: http://pid.geoscience.gov.au/geologicFeature/au/SU<stratno>

# Provinces:  http://pid.geoscience.gov.au/geologicFeature/au/PR<provno>