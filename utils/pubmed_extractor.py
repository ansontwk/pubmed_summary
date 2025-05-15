import metapub
import os    
import subprocess
import random
import time
def format_au(authorlist):
    if not authorlist:     #safety net
        return ""
    if len(authorlist) == 1:
        return authorlist[0]
    elif len(authorlist) >= 3:
        return f"{authorlist[0]} et al."
    else:
        return ",".join(authorlist)

def summarize_abstract(abstract):
    # Write abstract to tmp file
    with open("./tmp/tmp.txt", "w") as writefile:
        writefile.write(abstract)
    with open("./tmp/tmp.txt", "r") as tmpfile, open("./tmp/output.txt", "w") as outfile:
        subprocess.run("./extract_pub.sh", shell=True, stdin=tmpfile, stdout=outfile)
    summary = []
    with open("./tmp/output.txt", "r") as readfile:
        for line in readfile:
            summary.append(line.strip())
    return " ".join(summary).strip()

class pubmedextractor:
    def __init__(self, outprefix = 'pubmed_search', searchauthor = None, searchjournal = None, searchkeyword = None, searchstring = None):
        self.fetcher = metapub.PubMedFetcher()
        
        self.outprefix = outprefix
        self.outfile = self.get_outfile()
        
        self.searchauthor = searchauthor
        self.searchjournal = searchjournal
        self.searchkw = searchkeyword
        self.searchstring = searchstring
        
        self.search = self.format_keywords()
        self.pmids = []
        os.makedirs('./tmp', exist_ok=True)
    
    def get_outfile(self):
        filepath = self.outprefix + ".tsv"
        if os.path.exists(filepath):
            filepath = f"{self.outprefix}_{random.randint(0, 10000)}.tsv"
        return filepath
    
    def format_keywords(self):
        if self.searchstring:
            return self.searchstring
        author = f"{self.searchauthor}[au]" if self.searchauthor else ""
        kw = self.searchkw if self.searchkw else ""
        journal = f"{self.searchjournal}[ta]" if self.searchjournal else ""
        parts = [p for p in [kw, author, journal] if p]
        return " AND ".join(parts)
    
    def get_ids(self, retmax = 750):
        print(f"searching for: \n{self.search}")
        self.pmids = self.fetcher.pmids_for_query(self.search, retmax = retmax)
        print(f"Found {len(self.pmids)} articles.")    
        return self.pmids
    
    def process_abstract(self, abstract, shellscript = "./extract_pub.sh"):
        #calls extractpub
        with open("./tmp/tmp.txt", "w") as writefile:
            writefile.write(abstract)
        with open("./tmp/tmp.txt", 'r') as tmpfile, open('./tmp/output.txt', 'w', encoding= 'utf-8') as writefile:
            subprocess.run(shellscript, shell = True, stdin = tmpfile, stdout = writefile)
        summary = []
        with open("./tmp/output.txt", 'r') as readfile:
            for line in readfile:
                summary.append(line.strip())
        return " ".join(summary).strip()        
    
    def run_summary(self, pmids = None):
        if pmids is None:
            pmids = self.pmids
        print(f"Output file: {self.outfile}")
        with open(self.outfile, "w", encoding="utf-8") as f:
            f.write(f"# {self.search}\t{len(pmids)}\n")
            
            f.write("PMID\tTITLE\tAUTHORS\tKEYWORDS\tJOURNAL\tDOI\tYEAR\tLLM_summary\n")
            for pmid in pmids:
                #time.sleep(1)
                src = metapub.FindIt(pmid)
                authorstring = format_au(src.pma.authors)
                try:
                    abstract = " ".join(src.pma.abstract.split())
                    summary = self.process_abstract(abstract)
                except:
                    abstract = "Not available"
                    summary = "Not available"
                                           
                kw = src.pma.keywords if src.pma.keywords else " "
                f.write(f"{pmid}\t{src.pma.title}\t{authorstring}\t{kw}\t{src.pma.journal}\t{src.pma.doi}\t{src.pma.year}\t{summary}\n")
   
    def run(self):
        pmids = self.get_ids()
        self.run_summary(pmids)