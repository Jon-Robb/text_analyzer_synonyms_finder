from sys import argv
from argparse import ArgumentParser

class Options():
    def __init__(self):
        self.p = ArgumentParser(description="KNN")

        self.p.add_argument('-k', type=int, required=True)
        self.p.add_argument('--features', type=str, required=True)
        self.p.add_argument('--labels', type=str, required=True)
        self.p.add_argument('--enc', type=str, required=True)
        self.p.add_argument('--ponderation', type=int, required=True)
        self.p.add_argument('--normaliser', action="store_true")
        self.p.add_argument('--id', type=int, required=True)

        self.p.parse_args(args=argv[1:], namespace=Options)