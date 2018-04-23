from textblob import TextBlob

class TwitterHelper:

    def cleaner(self, item_text):

        try:
            cleaned_text = []
            for item in item_text:
                item = ' '.join(str(item).replace('\n', "").split())
                cleaned_text.append(item)



                return cleaned_text
        except TypeError:
            return None

    def translate(self, item_text):
        if item_text == None or item_text == "":
            return "null"
        elif isinstance(item_text, str):
            date = []
            for item in str(item_text).split(' '):
                try:
                    en_blob = TextBlob(item)
                    item = str(en_blob.translate(to='en'))
                    date.append(item)
                except:
                   date.append(item)
            return ','.join(date).replace(',',' ')
