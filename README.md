# Provinces data source for OGC LD API


### Provinces
http://services.ga.gov.au/gis/services/Australian_Geological_Provinces/MapServer/WFSServer?SERVICE=WFS&REQUEST=GetFeature&VERSION=1.1.0&maxFeatures=5&typeName=Australian_Geological_Provinces:AllProvinces

http://services.ga.gov.au/gis/services/Australian_Geological_Provinces/MapServer/WFSServer?SERVICE=WFS&REQUEST=GetFeature&VERSION=1.1.0&maxFeatures=5&typeName=Australian_Geological_Provinces:AllProvinces&startIndex=4&count=5

### Stratigraphic Units
#### Complex WFS representation
Examples: XML format

http://stratunits.gs.cloud.ga.gov.au/gsmlb/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=gsmlb%3AGeologicUnit&featureid=asud.gsml.geologicunit.332

HTML format

http://stratunits.gs.cloud.ga.gov.au/gsmlb/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=gsmlb%3AGeologicUnit&featureid=asud.gsml.geologicunit.332&outputformat=text%2Fhtml


Paging features:
http://stratunits.gs.cloud.ga.gov.au/gsmlb/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=gsmlb%3AGeologicUnit&startIndex=4&count=5

Limiting properties (not working):
http://stratunits.gs.cloud.ga.gov.au/gsmlb/wfs?service=WFS&version=2.0.0
    &request=GetFeature&typeName=gsmlb%3AGeologicUnit&startIndex=4&count=5
    &propertyName=identifier,name
    
http://stratunits.gs.cloud.ga.gov.au/gsmlb/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=gsmlb%3AGeologicUnit&startIndex=4&count=5&propertyName=gml:identifier,gml:name
