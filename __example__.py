import logging

from extractor.extractor import MasterExtractor
from extractor.document import Document

"""
This is a simple example how to use the extractor in combination with a dict in news-please format.

- Nothing is cached

"""

# don`t forget to start up core_nlp_host
# giveme5w1h-corenlp
# In Skopje, the German Foreign Minister expressed her support for an early EU accession
# My rent this month is $875 and I’m $200 short


titleshort = "The EU wants to deny the UK government its own border and migration policy, perhaps because it itself does not have a reasonable system."
data = "The EU wants to deny the UK government its own border and migration policy, perhaps because it itself does not have a reasonable system."

date_publish = '2016-11-10 07:44:00'

if __name__ == '__main__':
    extractor = MasterExtractor()
    doc = Document.from_text('The EU wants to send migrants back to Africa, the Middle East and Asia', date_publish)
    # doc = Document(titleshort, 'A total of 29 migrants swim across the border crossing in Ceuta', '', date_publish)

    doc = extractor.parse(doc)

    location_answer = doc.get_location_answer()
    print(location_answer)

    money_answer = doc.get_money_answer()
    print(money_answer)
    top_why_answer = doc.get_top_answer('why').get_parts_as_text()
    print(top_why_answer)

    #  top_when_answer = doc.get_top_answer('when').get_parts_as_text()
    #  top_why_answer = doc.get_top_answer('why').get_parts_as_text()
    # top_how_answer = doc.get_top_answer('how').get_parts_as_text()

#  print(top_when_answer)
#  print(top_where_answer)
#  print(top_why_answer)
#  print(top_how_answer)
