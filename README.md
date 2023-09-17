#### This project was init from a team's project made with [Cryptoblivious](https://github.com/cryptoblivious)
<br><br><br>
# Guide d'utilisation du programme d'analyse de texte

Ce programme d'analyse de textes offre plusieurs fonctionnalités, notamment le clustering par centroïdes, la recherche de synonymes et la génération d'une base de données de synonymes.

## Arguments de la ligne de commande

Voici les arguments de la ligne de commande que vous pouvez utiliser pour contrôler le fonctionnement du programme :

- `-e` : Évalue le texte.
- `-c` : Effectue du clustering par centroïdes sur le texte.
- `-n` : Spécifie le nombre maximal de mots à afficher par cluster à la fin de l'exécution.
- `-k` : Définit le nombre de centroïdes pour l'opération de clustering.
- `-t` : Définit la taille de la fenêtre de cooccurrence.
- `--enc` : Spécifie l'encodage du texte.
- `--chemin` : Spécifie le chemin du fichier texte à analyser.
- `-r` : Recherche des synonymes dans le texte.
- `-b` : Régénère la base de données de synonymes.
- `-v` : Affiche des informations supplémentaires pendant l'exécution du programme.
- `--knn` : Utilise l'algorithme KNN pour le clustering et spécifie le nombre de voisins à considérer.
- `--ponderation` : Utilise une pondération spécifique pour l'algorithme KNN.
- `--normaliser` : Normalise les vecteurs de mots.

## Exemples d'utilisation

Voici quelques exemples de la façon dont vous pouvez utiliser ce programme :

- Pour entraîner la base de donnée avec un texte :
  ```
  python main.py -e -t 5 --enc utf-8 --chemin /chemin/vers/fichier.txt -v
  ```
- Pour effectuer du clustering par centroïdes avec les cooccurrences de la base de données :
  ```
  python main.py -c -t 5 -k 3 -n 10 -v
  ```
- Pour rechercher des synonymes dans la base de données :
  ```
  python main.py -r -t 5 -v
  ```
- Pour régénérer la base de données :
  ```
  python main.py -b -v
  ```
- Pour utiliser l'algorithme KNN pour le clustering avec une pondération spécifique et la normalisation des distances :
  ```
  python main.py -c --knn 5 --ponderation 2 --normaliser -t 5 -k 3 -n 10 -v
  ```

## Remarques importantes

- Vous ne pouvez pas utiliser `-e`, `-r` et `-c` ensemble. Vous devez choisir l'une de ces options à la fois.
- L'option `--knn` ne peut être utilisée qu'avec `-c`.
- Les options `--ponderation` et `--normaliser` ne peuvent être utilisées qu'avec `--knn`.
- Lorsque vous utilisez `-e`, vous devez également spécifier `-t`, `--enc` et `--chemin`.
- Lorsque vous utilisez `-r`, vous devez également spécifier `-t`.
- Lorsque vous utilisez `-b`, aucun autre argument n'est authorisé, à l'exception de `-v` qui est facultatif.
- Lorsque vous utilisez `-c`, vous devez également spécifier `-t`, `-k`, et `-n`.
- Si vous ne fournissez aucun argument, le programme vous renverra une erreur. Veillez donc à spécifier au moins un argument lors de l'exécution du programme.
