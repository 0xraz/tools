import logging
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class Extractor:

    def __init__(self):
        logger.info("Initiating " + __name__)
        return

    def query_hosted_service(self, url, query, variables=None):

        if variables is not None:
            for variable in variables:
                print(variable)
                query = query.replace(str("$" + variable), str(variables[variable]))

        count = 1
        while count <= 10:
            response = requests.post(url, json={'query': query})

            if response.status_code == 200:
                response = response.json()
                if 'errors' in response:
                    errors = response['errors']
                    if len(errors) > 1:
                        for error in errors:
                            logger.debug(f"Response: {str(error['message'])}")
                    else:
                        logger.debug(f"Response: {str(errors['message'])}")
                elif 'data' in response:
                    return response['data']
                else:
                    logger.error('Unknown error getting response')
            else:
                logger.error(f'Query failed with status_code {str(response.status_code)}')

            count += 1
            logger.debug(f'Attempt {count}...')

        logger.error('Failed to complete query')
        return None
