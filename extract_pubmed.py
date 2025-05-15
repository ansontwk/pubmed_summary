from  utils.pubmed_extractor import pubmedextractor
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_prefix', default='search_summary', type=str)
    parser.add_argument('-a', '--author', type=str)
    parser.add_argument('-k', '--kw', type=str)
    parser.add_argument('-j', '--journal', type=str)
    parser.add_argument('--searchstring', type=str)
    return parser.parse_args()


test = '("SNP threshold" AND "transmission cluster") OR ("outbreak" AND "SNP") OR ("cgSNP" AND "outbreak") OR ("core genome SNP" AND "outbreak") OR ("SNP threshold" AND "outbreak") OR ("SNP" AND "transmission cluster") OR ("transmission cluster" AND "outbreak") NOT "Viruses"[MeSH Terms] NOT "Virus*" NOT "Viral*"'

def main():
    args = parse_args()
    summarizer = pubmedextractor(
        outprefix= args.output_prefix,
        searchauthor=args.author,
        searchkeyword=args.kw,
        searchjournal=args.journal,
        searchstring=args.searchstring
    )
    summarizer.run()
main()