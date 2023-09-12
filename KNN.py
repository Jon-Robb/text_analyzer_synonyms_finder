import numpy as np
from DAO_TP2 import DAO


def uniq(ordre, distance):
    return 1


def harm(ordre, distance):
    return 1 / (ordre + 1)


def dist(ordre, distance):
    return 1 / (distance**2 + 1)


PONDERATION = [uniq, harm, dist]


class KNN:
    def __init__(self, k, **kwargs):
        self.dao = DAO()
        self.k = int(k)
        ponderation = kwargs["ponderation"] if kwargs["ponderation"] else 0
        self.normalise = kwargs["normaliser"] if kwargs["normaliser"] else False
        self.ponderation = PONDERATION[int(ponderation)]
        # TODO : Implement normaliser
            
        try:
            self.dao.connect()
            self.word_labels = self.dao.get_words_types()
            self.word_dict = self.dao.get_words_dict()
            self.labels = set(self.word_labels.values())
        except Exception as e:
            print(e)
        finally:
            self.dao.disconnect()

    def evaluate_labels(self, cluster: list):
        votes = {label: 0 for label in self.labels}
        flipped_word_dict = {value: key for key, value in self.word_dict.items()}
        if self.normalise:
            distances = np.asarray(cluster)[:, 1]
            distance_normalized = self.normaliser(distances)
            cluster = np.asarray(cluster)
            cluster[:, 1] = distance_normalized
            cluster = list(cluster)
        for index in range(self.k):
            print(f"{flipped_word_dict[cluster[index][0]]} ({self.word_labels[cluster[index][0]]}) ----> {cluster[index][1]}")
            votes[self.word_labels[cluster[index][0]]] += self.ponderation(
                index, cluster[index][1]
            )
        # print the vote with the highest score
        print(f"Predicted class: {max(votes, key=votes.get)}")
        # print(f'Real class: {clusters[index]}')
        print()
        
    def normaliser(self, m):
        # 
        return (m.transpose()/np.linalg.norm(m)).transpose()
