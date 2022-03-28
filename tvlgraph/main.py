import logging
#import transformer.transformer as transformer
#import tvlgraph.extract.graphextractor as tvlgraph
import tvlgraph.extract.graphqueries as graphqueries

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def main():
    days = get_number_of_days()
    graphdata = graphqueries.TVL()
    data = graphdata.get_data(days)
    print(data)
    logger.debug("Done")

def get_number_of_days():
    while True:
        try:
            val = int(input("How many days in the past would you like collect data for (14): ") or 14)
            if val <= 0 or val > 100:
                print("You must choose a value between 1 and 100")
            else:
                break
        except ValueError:
            print("You much choose a value between 1 and 100")
    return val

if __name__ == "__main__":
    main()