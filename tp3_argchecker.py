import argparse

class TP3ArgsChecker:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Programme d'analyse d'un texte. Il permet de trouver des synonymes d'un mot donné dans le texte.")
        self.parser.add_argument('-e', action='store_true', help='argument pour évaluer le texte')
        self.parser.add_argument('-c', action='store_true', help='argument pour effectuer du clustering par centroïdes')
        self.parser.add_argument('-n', help='nombre maximale de mots à afficher par cluster (à la fin de l\'exécution)')
        self.parser.add_argument('-k', help='nombre de centroïdes, une valeur entière')
        self.parser.add_argument('-t', help='la taille de la fenêtre de cooccurrence')
        self.parser.add_argument('--enc', help='encodage du texte')
        self.parser.add_argument('--chemin', help='chemin du fichier texte')
        self.parser.add_argument('-r', action='store_true', help= 'argument pour rechercher les synonymes')
        self.parser.add_argument('-b', action='store_true', help='regénération de la base de données de synonymes')
        self.parser.add_argument('-v', action='store_true', help="argument pour afficher des informations supplémentaires")
        self.parser.add_argument('--knn', help="argument pour utiliser l'algorithme KNN et signifier le nombre de voisins à considérer")
        self.parser.add_argument('--ponderation', help="argument pour utiliser une pondération spécifique pour l'algorithme KNN")
        self.parser.add_argument('--normaliser', action='store_true', help="argument pour normaliser les vecteurs de mots")
        
        args = self.parser.parse_args() 
        all_args_none = all(arg is None or arg is False for _, arg in vars(args).items())
        all_args_none_but_b_or_v = all(arg is None or arg is False for key, arg in vars(args).items() if key not in ('b', 'v'))
        
        if all_args_none:
            self.parser.error("No arguments provided.")
            
        if args.e and args.r:
            self.parser.error("-e and -r cannot be used together.") 
            
        if args.e and args.c:
            self.parser.error("-e and -c cannot be used together.")
            
        if args.r and args.c:
            self.parser.error("-r and -c cannot be used together.")
            
        if args.knn and not args.c: 
            self.parser.error("--knn can only be used with -c")
        
        if (args.ponderation or args.normaliser) and not args.knn:
            self.parser.error("--ponderation and --normaliser can only be used with --knn")
            
        if args.e and not (args.t and args.enc and args.chemin):
            self.parser.error("-t, --enc, and --chemin are required when using -e")
            
        elif args.r and not args.t:
            self.parser.error("-t is required when using -r")
            
        elif args.b and not all_args_none_but_b_or_v:
            self.parser.error("No arguments are required when using -b. -v is optional.")
            
        elif args.c and not (args.t and args.k and args.n):
                self.parser.error("-t, -k, and -n are required when using -c")
                
    def get_args(self):
        return self.parser.parse_args()
    
    
    
    


