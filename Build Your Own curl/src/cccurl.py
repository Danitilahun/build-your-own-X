import argparse

parser = argparse.ArgumentParser(description="A simple tool to learn how to command line tool.")

parser.add_argument("url", help="Http url")

args = parser.parse_args()

print("URL" , args.url)