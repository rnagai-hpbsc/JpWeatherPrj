import argparse

def getParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='data/20200504.txt')
    return parser
