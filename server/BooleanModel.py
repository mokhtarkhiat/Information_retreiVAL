from main import importIndexList


if __name__ == '__main__':
    invertedfile : dict = importIndexList('data/index.pkl')

    for i in range(20):
        print(invertedfile)