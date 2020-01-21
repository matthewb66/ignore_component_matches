# Synopsys Ignore ExactFile Matches Script - ignore_exactfile_matches.py
# INTRODUCTION

This script is provided under an OSS license as an example of how to use the Black Duck APIs to ignore components matched by Signature scanning via the Exact File method. Note that this functionality (Exact File matching) will be deprecated by default in a future Black Duck release, removing the need to use this script.

It does not represent any extension of licensed functionality of Synopsys software itself and is provided as-is, without warranty or liability.

# DESCRIPTION

The `ignore_exactfile_matches.py` script ignores (or unignores) components matched by 'Exact File' selected by specified options.

A Black Duck project and project version must be specified, in addition to a flag defining the type of match and the file extension of matched files for components to be ignored.

The -u flag will unignore the specified components.

# PREREQUISITES

Python 3 and the Black Duck https://github.com/blackducksoftware/hub-rest-api-python package must be installed and configured to enable the Python API scripts for Black Duck prior to using this script.

An API key for the Black Duck server must also be configured in the `.restconfig.json` file in the package folder.

# INSTALLATION

Install the hub-rest-api-python package:

    git clone https://github.com/blackducksoftware/hub-rest-api-python.git
    cd hub-rest-api-python
    pip3 install -r requirements.txt
    pip3 install .
    
Copy the `ignore_exactfile_matches.py` script into the `examples` sub-folder within `hub-rest-api-python`.

Configure the hub connection in the `.restconfig.json` file within `hub-rest-api-python` - example contents:

    {
      "baseurl": "https://myhub.blackducksoftware.com",
      "api_token": "YWZkOTE5NGYtNzUxYS00NDFmLWJjNzItYmYwY2VlNDIxYzUwOmE4NjNlNmEzLWRlNTItNGFiMC04YTYwLWRBBWQ2MDFlMjA0Mg==",
      "insecure": true,
      "debug": false
    }

# USAGE

The `ignore_exactfile_matches.py` script can be invoked as follows:

    usage: ignore_components [-h] [-u] project version
                         {manual,directory,exactfile,filedependency} extension
    ignore_components: error: the following arguments are required: project, version, matchtype, extension

# EXAMPLE EXECUTION

Consider an example project/version (myproject/1.0), with the following components:

    Bootstrap (Twitter)/3.3.2	- 1 Match - Exact File
    cc-core/15.6.15.0 - 7 Matches - Exact Directory
    Commons IO/2.2 - 3 Matches - Transitive Dependency, Exact Directory
    Commons IO/2.4 - 3 Matches - Exact Directory
    Crowd/2.10.3 - 4 Matches - Exact File	
    datafari/4.2.1 - 12 Matches - Exact Directory	

The `Bootstrap (Twitter)/3.3.2` component has the following constituent files:

    boostrap.js
    
The `Crowd/2.10.3` component has the following constituent files:

    inputtransferselect.js
    optiontransferselect.js
    optiontransferselect.js
    webconsole.js

The following command will search for and ignore the Bootstrap and Crowd components (identified by Signature scanning with 'Exact File' match for .js files only):

    python3 examples/ignore_exactfile_matches.py myproject 1.0 exactfile .js

The following command will search for and UNignore the Bootstrap and Crowd components (identified by Signature scanning with 'Exact File' match for .js files only):

    python3 examples/ignore_exactfile_matches.py -u myproject 1.0 exactfile .js
   
