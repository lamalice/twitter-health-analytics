from textblob import TextBlob

def translate(self, item_text):
    trans_sent = []
    if item_text == None or item_text == "":
        return "Nothing to translate"
    if isinstance(item_text, str):
        try:
            en_blob = TextBlob(item_text)
            item_text = str(en_blob.translate(to='en'))
        except:
            return item_text
        return item_text
    for sent in item_text:
        try:
            en_blob = TextBlob(sent)
            trans_sent.append(str(en_blob.translate(to='en')))
        except:
            trans_sent.append(sent)
            pass
    return trans_sent