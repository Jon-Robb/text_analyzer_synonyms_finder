import numpy as np
from options import Options

SEP = '\t'

def uniq(ordre, distance): return 1
def harm(ordre, distance): return 1/(ordre+1)
def dist(ordre, distance): return 1/(distance**2 + 1)
PONDERATION = [uniq, harm, dist]

class KNN():
    def __init__(self, k, ch_feat, ch_etiq, enc, normaliser):
        self.k = k
        self.noms_feat, self.features = self.extract(ch_feat, enc, self.extract_features)
        self.noms_etiq, self.etiqs = self.extract(ch_etiq, enc, self.extract_label)
        if normaliser:
            self.features = self.normaliser(self.features)

    def extract(self, ch, enc, qqch):
        with open(ch, encoding=enc) as f:
            lignes = f.read().splitlines()

        noms = lignes[0].split(SEP)
        data = np.array([qqch(ligne) for ligne in lignes[1:]])

        return noms, data

    def extract_features(self, ligne):
        return [float(x) for x in ligne.split(SEP)]
    
    def extract_words(self, ligne):
        return ligne.split(SEP)

    def extract_label(self, ligne):
        return int(ligne)
    
    def normaliser(self, m):
        return (m.transpose()/np.linalg.norm(m, axis = 1)).transpose()

    def knn(self, id, ponderation):
        distances = []
        for index, coord in enumerate(self.features):
            if index != id:
                distance = np.linalg.norm(coord - self.features[id])
                etiquette = self.noms_etiq[self.etiqs[index]]
                distances.append( (distance, etiquette) )

        distances = sorted(distances)
        votes = {nom:0 for nom in self.noms_etiq}
        for ordre, (distance, etiq) in enumerate(distances[:self.k]):
            votes[etiq] += ponderation(ordre, distance)
        votes = sorted(votes.items(), key=lambda t:t[1], reverse=True)

        # print(distances)
        print(f'Real class: {self.noms_etiq[self.etiqs[id]]}')
        print(votes)


def main():
    opts = Options()

    knn = KNN(opts.k, opts.features, opts.labels, opts.enc, opts.normaliser)

    # print(knn.noms_feat)
    # print(knn.features)
    # print(knn.noms_etiq)
    # print(knn.etiqs)
    # print()

    knn.knn(opts.id, PONDERATION[opts.ponderation])

    return 0

if __name__ == '__main__':
    with open('C62\TP3\knn_prof\Lexique382.tsv') as f:
        lines = f.read().splitlines()
        for line in lines[1:10]:
            print(line.split('\t')[0], line.split('\t')[3])
    
    
        
        
    # quit(main())