import argparse
import metapub
import os
import random
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output_prefix', default = 'search_summary', type = str)
parser.add_argument('-a', '--author', type = str)
parser.add_argument('-k', '--kw', type = str)
parser.add_argument('-j', '--journal', type = str)
parser.add_argument('--searchstring', type = str)
args = parser.parse_args()

if args.searchstring:
    search = args.searchstring
else:    
    author = ""
    kw = ""
    journal = ""

    if args.author:
        author = args.author + "[au]"
    if args.kw:
        kw = args.kw
    if args.journal:
        journal = args.journal + "[ta]"
    
    search = kw + " AND " + author + " AND " + journal
search = search.strip(" AND ")
print(f"Searching for: {search}")


OUTFILE = args.output_prefix + ".tsv"
if os.path.exists(OUTFILE):
    OUTFILE = args.output_prefix + "_" + str(random.randint(0, 1000)) + ".tsv"
print("Output file: " + OUTFILE)

def main():
    fetch = metapub.PubMedFetcher()
    articles = fetch.pmids_for_query(search, retmax= 500)
    print(f"Found {len(articles)} articles")
    with open(OUTFILE, "w") as f:
        f.write("PMID\tTITLE\tAUTHORS\tABSTRACT\tKEYWORDS\tJOURNAL\tDOI\tYEAR\tLLM_summary\n")
        for pmid in articles:
            
            src = metapub.FindIt(pmid)
            authorstring = ",".join(src.pma.authors)
            try:
                abstract = " ".join(src.pma.abstract.split())
            except:
                abstract = "Not available"
            
            #extract the ollama summarised paragraph
            with open("./tmp/tmp.txt", "w") as writefile:
                writefile.write(f"{abstract}")
            with open("./tmp/tmp.txt", "r") as tmpfile, open("./tmp/output.txt", "w") as outfile:
                subprocess.run("./extract_pub.sh", shell=True, stdin=tmpfile, stdout=outfile)
            summary = []
            with open("./tmp/output.txt", "r") as readfile:
                for line in readfile:
                    summary.append(line.strip())
            summary = " ".join(summary).strip()
            
            #============== 
            f.write(f"{pmid}\t{src.pma.title}\t{authorstring}\t{abstract}\t{src.pma.keywords}\t{src.pma.journal}\t{src.pma.doi}\t{src.pma.year}\t{summary}\n")
main()