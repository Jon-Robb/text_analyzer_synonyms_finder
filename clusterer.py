import numpy as np
import time
import copy

class Clusterer:
    def __init__(self, co_matrix:list, k_clusters:int, verbose:bool):
        self.co_matrix = co_matrix
        self.k_clusters = int(k_clusters)
        self.verbose = verbose
    
        self.centroid_members = [[] for _ in range(self.k_clusters)]
        
        self.n_iterations = 0
        self.n_changes = 0
        self.stabilized = False
        
        
    def cluster(self):
        # new_clusters = np.full(clusters.shape, len(centroids) + 1, dtype=np.int64)
        # self.evaluate_changes(clusters, new_clusters)
        
        if self.verbose:
            print("Évaluation des clusters en cours, veuillez patienter...\n")
            start_time = time.perf_counter()
        while not self.stabilized:
            if self.verbose:
                iteration_time = time.perf_counter()
            self.n_iterations += 1
            
            if self.n_iterations == 1:
                centroids = self.initialize_centroids()
                new_clusters = self.evaluate_distance(centroids)
                clusters = np.full(new_clusters.shape, -1, dtype=np.int64)

            else:
                centroids = self.calculate_new_centroids(clusters)
                new_clusters = self.evaluate_distance(centroids)
                
            self.evaluate_changes(clusters, new_clusters)
            if self.verbose:
                print("Itération " + str(self.n_iterations) + " effectuée en " + str(round(time.perf_counter() - iteration_time, 3)) + " secondes (" + str(self.n_changes) + " changements)\n")
                for i in range(self.k_clusters):
                    print("Il y a " + str(np.count_nonzero(np.where(new_clusters == i)[0])) + " mots appartenant au centroïde " + str(i))
                print("\n**************************************\n")
                                  
            if not self.stabilized :
                clusters = copy.deepcopy(new_clusters)
            else :
                if self.verbose:
                    print("Clustering effectué en " + str(self.n_iterations) + " itérations en un temps de "+ str(round(time.perf_counter() - start_time, 3)) + " secondes.\n")
                return self.sort_centroid_members()
                
    
    def initialize_centroids(self):
        centroids = np.zeros((self.k_clusters, self.co_matrix.shape[1]))
        for i in range(self.k_clusters):
            centroids[i] = self.co_matrix[i]
        return centroids
    
                  
    def evaluate_distance(self, centroids):
        # start_time = time.perf_counter()
        words_in_cluster = np.arange(len(self.co_matrix))
        self.distances = [np.sum((self.co_matrix - centroid )**2 , axis=1) for centroid in centroids]
        words_in_cluster = np.argmin(self.distances, axis=0)
        # print("Temps d'évaluation des distances : " + str(time.perf_counter() - start_time) + " secondes\n") 
        return words_in_cluster
    
    def evaluate_distance_by_least_squares(self, centroid):
        # start_time = time.perf_counter()
        sum = np.sum((self.co_matrix - centroid)**2, axis=1)
        # print("Temps d'évaluation des distances : " + str(time.perf_counter() - start_time) + " secondes\n") 
        return sum
    
    def evaluate_changes(self, clusters, new_clusters):
        # start_time = time.perf_counter()
        self.n_changes = np.sum(np.not_equal(clusters, new_clusters))
        if self.n_changes == 0:
            self.stabilized = True
        # print("Temps d'évaluation des changements : " + str(time.perf_counter() - start_time) + " secondes\n")
        
     
    def apply_changes(self):
        # start_time = time.perf_counter()
        self.starting_centroid_members = self.centroid_members
        self.centroid_members = [[] for _ in range(self.k_clusters)]
        self.n_changes = 0
        # print("Temps d'application des changements : " + str(time.perf_counter() - start_time) + " secondes\n")
        
    def calculate_new_centroids(self, clusters):
        # start_time = time.perf_counter()
        centroids = np.zeros((self.k_clusters, self.co_matrix.shape[1]))
        for i in range(self.k_clusters):
            # centroid = np.array(self.starting_centroid_members[i], dtype=int)
            centroid_members = np.where(clusters == i)[0]
            # get the average of the vectors in the cluster
            centroids[i] = np.mean(self.co_matrix[centroid_members], axis=0)
            # centroids[i] = np.mean(self.co_matrix[centroid_members])
        # print("Temps de calcul des nouveaux centroïdes : " + str(time.perf_counter() - start_time) + " secondes\n")
        return centroids
            
    def sort_centroid_members(self):
        # start_time = time.perf_counter()
        distances_from_centroids = np.transpose(self.distances)
        for i, distances in enumerate(distances_from_centroids):
            self.centroid_members[np.argmin(distances)].append([i, distances[np.argmin(distances)]])
        #sort the members of each centroid by their distance from the centroid
        self.centroid_members = [sorted(self.centroid_members[i], key=lambda x: x[1]) for i in range(self.k_clusters)]
        # print("Temps de tri des membres des centroïdes : " + str(time.perf_counter() - start_time) + " secondes\n")
        return self.centroid_members