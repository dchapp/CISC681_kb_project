import argparse
import os
import sys

from Rule import *


def main():
    parser = argparse.ArgumentParser(description="An inference engine for poisonous mushroom identification.")
    parser.add_argument("input", nargs=1, help="File describing mushroom or symptoms")
    parser.add_argument("-m", "--mode", nargs=1, default=[], help="How to process your query.")
    args = parser.parse_args()


    r = Rule(0,0)
    print r.a
    print r.c
    print type(r)


main()
