##Use biopython to download the first 10 genbank records
##for the organism Mus musculus
##Save the results to this outfile:
outfile="1st_10_mouse_genbank_records.gb"

from Bio import Entrez

Entrez.email = "reneefonseca@mail.usf.edu"

handle = Entrez.esearch(db = "nucleotide",term = "Mus musculus", retmax = 10, idtype = "acc", usehistory = "y")

search_results = Entrez.read(handle)
handle.close()

webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"]

records = 10
batch = 10

from urllib2 import HTTPError 
import time

out_handle = open(outfile,"w") 

for start in range (0,records, batch):
    end = min(records, start+batch) 
    print "Downloading record %i to %i" % (start+1, end)
    attempt = 0
    while attempt <3:
        attempt+=1
        try:
            fetch_handle = Entrez.efetch(db = "nucleotide", rettype = "gb", retmode = "text", retstart = start, retmax = batch, webenv = webenv, query_key = query_key, idtype = "acc")
        except HTTPError as err:
            if 500 <= err.code <= 599:
                print "Server error %s" %err
                print "Attempt %i of 3" %attempt
            else:
                raise
data = fetch_handle.read()
fetch_handle.close()
out_handle.write(data)
out_handle.close()