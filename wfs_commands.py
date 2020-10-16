import requests


uri = "http://stratunits.gs.cloud.ga.gov.au/gsmlb/wfs"
# params = {
#     "service": "WFS",
#     "version": "2.0.0",
#     "request": "GetFeature",
#     "typeName": "gsmlb:GeologicUnit",
#     "featureid": "asud.gsml.geologicunit.332"
# }
# r = requests.get(uri, params=params)
# print(r.text)

xml = """<?xml version="1.0" ?>
<wfs:GetFeature
    service="WFS"
    version="2.0.0"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:wfs="http://www.opengis.net/wfs/2.0" 
    xmlns:cit="http://standards.iso.org/iso/19115/-3/cit/1.0" 
    xmlns:gco="http://standards.iso.org/iso/19115/-3/gco/1.0" 
    xmlns:gml="http://www.opengis.net/gml/3.2" 
    xmlns:gmlsf="http://www.opengis.net/gmlsf" 
    xmlns:gsmlb="http://www.opengis.net/gsml/4.1/GeoSciML-Basic" 
    xmlns:gsmle="http://www.opengis.net/gsml/4.1/GeoSciML-Extension" 
    xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/1.0" 
    xmlns:swe="http://www.opengis.net/swe/2.0" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://standards.iso.org/iso/19115/-3/mrl/1.0 https://standards.iso.org/iso/19115/-3/mrl/1.0/mrl.xsd http://standards.iso.org/iso/19115/-3/cit/1.0 https://standards.iso.org/iso/19115/-3/cit/1.0/cit.xsd http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd http://www.opengis.net/gsml/4.1/GeoSciML-Extension http://schemas.opengis.net/gsml/4.1/geoSciMLExtension.xsd http://www.opengis.net/gsml/4.1/GeoSciML-Basic http://schemas.opengis.net/gsml/4.1/geoSciMLBasic.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd"
   >

</wfs:GetFeature>"""
r = requests.post(uri, data=xml, headers={'Content-Type': 'application/xml'})
print(r.text)

"""
        <ogc:PropertyIsEqualTo>
            <ogc:PropertyName>gsmlb:GeologicUnit/gml:identifier</ogc:PropertyName>
            <ogc:Literal>http://pid.geoscience.gov.au/feature/asc/gsml/geologicalunit/332</ogc:Literal>
        </ogc:PropertyIsEqualTo>
        
              <ogc:PropertyName>gml:identifier</ogc:PropertyName>
      <ogc:PropertyName>gml:name</ogc:PropertyName>
      
   <wfs:Query typeName="gsmlb:GeologicUnit">
      <ogc:Filter>
        <ogc:PropertyIsEqualTo>
            <ogc:PropertyName>ID</ogc:PropertyName>
            <ogc:Literal>asud.gsml.geologicunit.332</ogc:Literal>
        </ogc:PropertyIsEqualTo>
      </ogc:Filter>
   </wfs:Query>      
"""