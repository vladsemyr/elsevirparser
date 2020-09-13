"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
    
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']

## Initialize doc search object using ScienceDirect and execute search, 
#   retrieving all results

doc_srch = ElsSearch("DSP AND PUBYEAR = 2020",'sciencedirect')
doc_srch.execute(client, get_all = False)
print ("doc_srch has", doc_srch.tot_num_res, "results.")