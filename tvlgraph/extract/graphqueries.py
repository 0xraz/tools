import logging
import graphextractor as graphextractor
from datetime import datetime, timezone, timedelta, time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class TVL:
    """
    A class that writes graphql queries for 0xNODES subgraphs to obtain
    total value locked across chains
    """
    def __init__(self): 
        logger.info("Initiating " + __name__)
        self.results = graphextractor.Extractor()
        return

    def get_data(self, days=14):
        logger.info(f"Getting date for the last {str(days)} days")

        tvl_data = self.get_tvl_data('token0', days)

    def get_tvl_data(self, token_part, days):
        
        logger.debug(f"Getting 0xNODES subgraph data for {str(token_part)} ...")
        # TODO: create dict of { chain: "subgraph url" }
        url = "https://api.thegraph.com/subgraphs/name/0xnodes/system11"
        skip = 0
        data_found = True
        graph_data = []
        try:
            while data_found:
                logger.debug("Running query with skip value of " + str(skip))
                query = """{
                  pairDayDatas(first:1000, skip:<skip> orderBy: date, orderDirection:desc, where: {<token_part>:"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", date_gte: <timestamp_start_date>, date_lte: <timestamp_end_date>}) {
                    id
                    date
                    pair {
                     id
                     name
                    token0{
                      id
                      name
                    }
                    token1{
                      id
                      name
                    }
                    }
                    volumeToken0
                    volumeToken1
                    volumeUSD
                    reserve0
                    reserve1
                    reserveUSD 
                  }
                }"""
                query = query.replace('<skip>', str(skip))

                # Default date range with no user input is Start: 14 days ago, End: today
                utc_time_today = datetime.combine(datetime.now(timezone.utc), time.min) # datetime of midnight today in utc
                utc_time_today = utc_time_today.replace(tzinfo=timezone.utc) # add utc tag before timetsamp conversion
                # timestamp_today = int(datetime.timestamp(utc_time_today)) # convert to unix timestamp
                # utc_time_14d = datetime.now(timezone.utc) + timedelta(days=-14)  # datetime of now minus 14 days ago
                # utc_time_14d = datetime.combine(utc_time_14d, time.min)  # change datetime to midnight of that day
                # utc_time_14d = utc_time_14d.replace(tzinfo=timezone.utc) # add utc tag before timetsamp conversion
                # timestamp_14d = int(datetime.timestamp(utc_time_14d))  # convert to unix timestamp

                # timestamp_start_date = timestamp_14d # Default, but replace with user input if available
                timestamp_end_date = int(datetime.timestamp(utc_time_today)) # Default, but replace with user input if available
                timestamp_start_date = int(datetime.timestamp(datetime.now(timezone.utc) - timedelta(days=days)))

                query = query.replace('<timestamp_start_date>', str(timestamp_start_date))
                query = query.replace('<timestamp_end_date>', str(timestamp_end_date))
                query = query.replace('<token_part>', token_part)

                response = self.graphextractor.query_hosted_service(url, query)

                if len(response['pairDayDatas']) > 0:
                    for entry in response['pairDayDatas']:
                        graph_data.append(entry)

                if len(response['pairDayDatas']) == 1000:
                    skip += 1000
                    if skip == 6000:
                        data_found = False
                else:
                    data_found = False

            return graph_data

        except Exception as ex:
            logger.error("Error while querying data:", ex)
            return None

    def get_mcv1_data(self):
        logger.debug("Getting SushiSwap MCV1 pools rewards data...")

        url = "https://api.thegraph.com/subgraphs/name/sushiswap/master-chef"
        skip = 0
        data_found = True
        graph_data = []
        try:
            while data_found:
                logger.debug("Running query with skip value of " + str(skip))
                query = """{
                  pools (first: 1000) {
                    id
                    pair
                    allocPoint 
                  }
                }"""
                query = query.replace('<skip>', str(skip))
                response = self.thegraph.query_hosted_service(url, query)

                if len(response['pools']) > 0:
                    for entry in response['pools']:
                        graph_data.append(entry)

                if len(response['pools']) == 1000:
                    skip += 1000
                    if skip == 6000:
                        data_found = False
                else:
                    data_found = False

            return graph_data

        except Exception as ex:
            logger.error("Error while querying data:", ex)
            return None