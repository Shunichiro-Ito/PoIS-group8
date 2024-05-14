class MecabTokenizer:
    def __init__(self):
        self.wakati = MeCab.Tagger('-Owakati')
        self.wakati.parse('')

    def tokenize(self, line):
        txt = self.wakati.parse(line)
        txt = txt.split()
        return txt

    def mecab_tokenizer(self, line):
        node = self.wakati.parseToNode(line)
        keywords = []
        while node:
            if node.feature.split(",")[0] == "名詞":
                keywords.append(node.surface)
            node = node.next
        return keywords