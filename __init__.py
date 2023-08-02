import logging

from extractor.extractor import MasterExtractor
from extractor.document import Document

"""
This is a simple example how to use the extractor in combination with a dict in news-please format.

- Nothing is cached

"""

# don`t forget to start up core_nlp_host
# giveme5w1h-corenlp

titleshort = "Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008."

title = "Taliban attacks German consulate in northern Afghan city of Mazar-i-Sharif with truck bomb"
lead = "The death toll from a powerful Taliban truck bombing at the German consulate in Afghanistan's Mazar-i-Sharif city rose to at least six Friday, with more than 100 others wounded in a major militant assault."
text = """The Taliban said the bombing late Thursday, which tore a massive crater in the road and overturned cars, was a "revenge attack" for US air strikes this month in the volatile province of Kunduz that left 32 civilians dead.

The explosion, followed by sporadic gunfire, reverberated across the usually tranquil northern city, smashing windows of nearby shops and leaving terrified local residents fleeing for cover.


"""
date_publish = '2016-11-10 07:44:00'

if __name__ == '__main__':
    print('aa')
    # giveme5w setup - with defaults
    extractor = MasterExtractor()
    doc = Document.from_text(titleshort, date_publish)

    doc = extractor.parse(doc)

    top_who_answer = doc.get_top_answer('who').get_parts_as_text()
    top_what_answer = doc.get_top_answer('what').get_parts_as_text()
  #  top_when_answer = doc.get_top_answer('when').get_parts_as_text()
  #  top_where_answer = doc.get_top_answer('where').get_parts_as_text()
  #  top_why_answer = doc.get_top_answer('why').get_parts_as_text()
   # top_how_answer = doc.get_top_answer('how').get_parts_as_text()

    print(top_who_answer)
    print(top_what_answer)
  #  print(top_when_answer)
  #  print(top_where_answer)
  #  print(top_why_answer)
  #  print(top_how_answer)
