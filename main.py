"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json

from threading import Thread
    
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']


class Article:
    _begin_year = 2000
    _end_year = 2020
    _filename = "out.csv"
    _similar = []
    
    @classmethod
    def default_init(cls, d):
        Article._begin_year = d["begin_year"]
        Article._end_year = d["end_year"]
        Article._filename = d["output_filename"]
    
    def __init__(self, title: str, d: dict):
        self._title = title
            
        if "begin_year" in d:
            self._begin_year = d["begin_year"]
        
        if "end_year" in d:
            self._end_year = d["end_year"]
        
        if "output_filename" in d:
            self._filename = d["output_filename"]
        
        if "similar" in d:
            self._similar = d["similar"]
        
        self._new_title = self._title
        if "title" in d:
            self._new_title = d["title"]
    
    def search(self):
        search_string_without_year = f"({self._title})" + "".join(list(f" OR ({x})" for x in self._similar))
        
        for year in range(self._begin_year, self._end_year + 1):
            search_string_year = f" AND PUBYEAR = {year}"
            
            doc_srch = ElsSearch(search_string_without_year + search_string_year,'sciencedirect')
            doc_srch.execute(client, get_all = False)
            
            with open(self._filename, "a") as f:
                f.write(f"{self._new_title};{year};{doc_srch.tot_num_res}\n")
    
    def clean_file(self):
        with open(self._filename, "w") as _:
            pass
    
    @property
    def filename(self):
        return self._filename


with open("search.json", "r") as f:
    search_obj = json.load(f)

Article.default_init(search_obj["default"])
articles = list(Article(key, val) for (key,val) in search_obj["titles"].items())

for a in articles:
    a.clean_file()

for a in articles:
    a.search()




# https://www.sciencedirect.com/search?qs=DSP%20processor%20asd
# https://dev.elsevier.com/sc_search_tips.html