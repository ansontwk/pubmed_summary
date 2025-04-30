#metapub fetcher
#update ollama: curl -fsSL https://ollama.com/install.sh | sh
##only open access articles are available
##version 2 now supports summarised abstract based on ollama 3.2 with customised config
##refer to ollama_config

#setup for ollama
1. create ollama instance
ollama create pubmed -f ./ollama_config

2. test ollama
ollama run pubmed "Your test prompt"

3. Load prompt from file
ollama run pubmed < PATH/TO/FILE/WITH/PROMPT


Reference:
#	https://github.com/metapub/metapub

dependencies:
	python>=3.9 (tested on python 3.9)
	
how to install:
#	pip install metapub

Search terms should follow:
# https://pubmed.ncbi.nlm.nih.gov/help/


#import metapub
#fetcher = metapub.PubMedFetcher() #parser

#fetchterms
[au] = AUTHORS
[dp] = date
[ta] = abbreviated journal name

### In terminal:
Make sure you have a ./tmp directory

python extractpubmed.py -k "1918" -a "pl ho" -o "test_output"
will search for "1918", author by "pl ho" and output all entries to a file called test_output.tsv in the same folder.

Alternatively:
python extractpubmed.py --kw "1918 AND pl ho [au]" -o "test_output"
will yield the same search result


#### Example search terms:
1. Searching for keywords "PLM" and "NLP" within 2024.
python extractpubmed.py --kw "NLP AND PLM AND 2024/01/01:2024/12/31[dp]" 

	#NLP and PLM # keywords
	#2024/01/01 : 2024/12/31 #Follows a YYYY/MM/DD format, colon to get range
	#[dp]: date field for tag

2. Searching for keywords "protein language model" within 2024 in Briefing in bioinformatics only.
python extractpubmed.py --kw 'protein language model AND Brief. Bioinform [TA] AND 2024/01/01:2024/12/31[dp]'

