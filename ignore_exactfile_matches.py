#!/usr/bin/env python

#
# Script to ignore specified components
# Use internal API - will need to be updated once external API available in 2019.10

import argparse
import logging
#import json
#import sys

from blackduck.HubRestApi import HubInstance

matchtypes = {
	'manual': 'MANUAL_BOM_COMPONENT',
    'directory': 'FILE_EXACT',
    'exactfile': 'FILE_EXACT_FILE_MATCH',
	'filedependency': 'FILE_DEPENDENCY'
}

matchtype_list = list(matchtypes.keys())

parser = argparse.ArgumentParser(description='Ignore (or uningnore) components with specific match types and optional matched file extension', prog='ignore_components')
parser.add_argument('-u', action='store_false', default=True, dest='ignore', help='Unignore already ignored components')
parser.add_argument("project", type=str, help="Black Duck project name")
parser.add_argument("version", type=str, help="Black Duck project version name")
parser.add_argument("matchtype", type=str, choices=matchtype_list, help="Choose the match type from this list")
parser.add_argument("extension", type=str, help="Matched file extension", default='')

args = parser.parse_args()
if not args.ignore:
    print("Unignore is not supported yet - expected within v2019.10 release")
    exit()

hub = HubInstance()

logging.basicConfig(filename='ignore_components.log',level=logging.DEBUG)
#logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', stream=sys.stdout, level=logging.INFO)
logging.getLogger("requests").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)

project = hub.get_project_by_name(args.project)
version = hub.get_version_by_name(project, args.version)

if version is None:
	print("Project {} Version {} does not exist".format(args.project, args.version))
	exit()
	
#
# Get the BOM component entries 
version_url = version['_meta']['href']
bom_url = "/".join(version_url.split("/")[0:3]) + "/api/v1/releases/" + version_url.split("/")[-1] + "/component-bom-entries?limit=1000"
if not args.ignore:
    bom_url = bom_url + "&aggregationEntityType=RL&inUseOnly=true&filter=bomInclusion%3Atrue"

print(bom_url)
bom = hub.execute_get(bom_url)
          
if bom.status_code != 200:
    logging.error("Failed to retrieve matchedfiles, status code: {}".format(bom.status_code))
    exit()
bom_components = bom.json()['items']

#print(json.dumps(bom_components, indent=4, sort_keys=True))

def _ignorecomponent(component_info, ignorevalue):
    custom_headers = {
        'Content-Type':'application/json'
    }
    component_info['ignored'] = True        
    component_list = [ component_info ]
    
    #print(json.dumps(component_list, indent=4, sort_keys=True))
    response = hub.execute_put(bom_url, component_list, custom_headers=custom_headers)
    #response = hub.execute_put(bom_url, component_info)
    if response.status_code == 200:
        logging.info("Successfully ignored component {} version {}".format(component_info['projectName'], component_info['releaseVersion']))
        print("Successfully ignored component {} version {}".format(component_info['projectName'], component_info['releaseVersion']))
        return(True)
    else:
        logging.info("COULD NOT ignore component {} version {}".format(component_info['projectName'], component_info['releaseVersion']))
        print("COULD NOT ignore component {} version {}".format(component_info['projectName'], component_info['releaseVersion']))
        return(False)

#components = hub.get_version_components(version)
print("Working on project {}, version {}.".format(args.project, args.version))
ignored_count = 0
component_count = 0
for component in bom_components:
    component_count += 1
    componentmatch = False
    if component['matchTypes'][0] == matchtypes[args.matchtype]:
        #print("{}, {}".format(component['projectName'], component['matchTypes']))
        if args.extension != '' and args.ignore:
            #
            # Get matches files URL
            allmatchfiles = True
            if '_meta' in component:
                matchedfiles_url = component['_meta']['links'][4]['href']
                matches = hub.execute_get(matchedfiles_url)            
                if matches.status_code != 200:
                    logging.error("Failed to retrieve matchedfiles, status code: {}".format(matches.status_code))
                    exit
                
                for matchentry in matches.json().get('items'):
                    path = matchentry['filePath']['path']
                    if path.find(args.extension) != len(path) - len(args.extension):
                        #print(" >> {}".format(matchentry['filePath']['path']))
                    #else:
                        allmatchfiles = False
                        #print("file non-match")
                        break
    
            if allmatchfiles == True:
                componentmatch = True
        
        else:
            componentmatch = True
    
        if _ignorecomponent(component, args.ignore):
            ignored_count += 1

if args.ignore:
    print("Ignored {} components out of {} total".format(ignored_count, component_count))
else:
    print("Unignored {} components out of {} ignored".format(ignored_count, component_count))
       