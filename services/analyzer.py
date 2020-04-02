import json


with open('./config.json') as f:
  config = json.load(f)

class Analyzer:

    def __init__(self, data):
        super().__init__()
        self.data = data

    def get(self):
      #Matrice de correlation
      pass

    def build(self):
        # print(self.data.groupby('Processeur').mean())
        self.data.to_csv(r'Phone.csv', index = None, header=True)

