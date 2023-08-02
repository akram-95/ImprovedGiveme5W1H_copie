from stanza.server import CoreNLPClient, StartServer

# example text
print('---')
print('input text')
print('')
text = "Chris Manning is a nice person. Chris wrote a simple sentence. He also gives oranges to people."
print(text)
# set up the client
print('---')
print('starting up Java Stanford CoreNLP Server...')
# set up the client
host = "http://localhost:9000"
with CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'depparse', 'coref'], timeout=30000,
                   memory='16G', endpoint=host,
                   start_server=StartServer.DONT_START) as client:
    # submit the request to the server
    ann = client.annotate(text)
    # get the first sentence
    sentence = ann.sentence[0]
print('---')
print('named entity tag of token')

# get an entity mention from the first sentence
print('---')
print('first entity mention in sentence')

# access the coref chain
print('---')
print('coref chains for the example')

# Use tokensregex patterns to find who wrote a sentence.
pattern = '([ner: PERSON]+) /wrote/ /an?/ []{0,3} /sentence|article/'
matches = client.tokensregex(text, pattern)
##print(matches)
pattern = '{word:wrote} >nsubj {}=subject >dobj {}=object'
pattern = '[{ner:"MONEY"}]+'

matches = client.tokensregex('i have 100000 euro', pattern)
print(matches)

pattern = '[{ner:"NUMBER"}]+ [{ner:"LOCATION"}]+ [{ner:"CITY"}]+ /,/[] [{ner:"NUMBER"}]+'

matches = client.tokensregex('i lived in Wittekamp20, EG Mitte, 30163 Hannover', pattern)
print(matches)
