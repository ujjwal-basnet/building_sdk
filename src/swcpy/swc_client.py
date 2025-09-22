## minimal sdk , just to call the health check  of the swc api 
import httpx 
import swcpy.swc_config as config 
from .schemas import League, Player, Performance 
from typing import List
import backoff 
import logging 

logger= logging.getLogger(__name__) 
class SWCClient:
    """ Interacts with the swc API 
        This SDK class simplifies the process of using the SWC fantasy 
        football API it suports all the functions of swc api and return validated data types
        
        Typicall usages examples 
        
        client=  SWCClient()
        response= client.get_health_check() """
    
    HEALTH_CHECK_ENDPOINT = "/"
    LIST_LEAGUES_ENDPOINT = "/v0/leagues/"
    LIST_PLAYERS_ENDPOINT = "/v0/players/"
    LIST_PERFORMANCES_ENDPOINT = "/v0/performances/"
    LIST_TEAMS_ENDPOINT = "/v0/teams/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"
        
    BULK_FILE_BASE_URL = "https://github.com/ujjwal-basnet/building_api/tree/main/bulk"

    def ___init__(self, input_config:config.SWCConfig):
        """ class constructor that sets variable form configuration object"""
        logger.debug(f"Bulk file base URL : {self.BULK_FILE_BASE_URL}")
        logger.debug(f"Input config : {input_config}")
        
        self.swc_base_url= input_config.swc_base_url 
        self.backoff = input_config.swc_backoff
        self.bulk_file= input_config.swc_bulk_file_format
        self.bulk_file_format= input_config.swc_bulk_file_format

        self.BULK_FILE_NAMES= {
            "players": "player_data",
            "leagues": "leauge_data",
            "performances": "performance_data",
            "team_payers": "team_player_data",

        } 


        if self.backoff:
            self.call_api= backoff.on_exception(
                wait_gen= backoff.expo , 
                exception= (httpx.RequestError, httpx.HTTPStatusError),
                max_time= self.backoff_max_time,
                jutter= backoff.random_jitter,
            )(self.call_api)

        if self.bulk_file_format.lower()== "parquet":
            self.BULK_FILE_BASE_URL = {
                key: value + ".paraquet" for key , value in self.BULK_FILE_NAMES.items()
            }
        
        else :
            self.BULK_FILENAMES = {
                key: value + ".csv" for key,  value in self.BULK_FILE_NAMES.items()
            }


        logger.debug(f"Bulk file dictionary : {self.BULK_FILE_NAMES}")



    def call_api(self, api_endpoint: str , 
                 api_params: dict= None , 
                 ) -> httpx.Response: 
        """ Makes API calls and logs errors"""
        if api_params: 
            api_params= {key:val for key , val in api_params.items() if val is not None }

        
        try : 
            with httpx.Client(base_url= self.swc_base_url) as client:
                logger.debug(f"base_url: {self.swc_base_url}, api_endpoint: {api_endpoint}, api_params: {api_params}")

        except httpx.HTTPStatusError as e : 
            logger.error(f"HTTP status error occured: {e.response.status_code}")
            raise 

        except httpx.ReadError as e : 
            logger.error(f"Request error occured: {str(e)}")

            raise 

    
    def get_health_check(self)-> httpx.Response:
        """checks if Api is running and healthy
        
        calls the [api health check endpoint ], return a standard message if the api is running normally .
        
        can be used to check the status of api before making more complicated api calls
        

        Returns: 
        An httpx.Response object that contains http status , 
        json response and other information recevied from the api
        """
        logger.debug("Entered Health check")
        endpoint_url= self.HEALTH_CHECK_ENDPOINT 
        return self.call_api(endpoint_url)
    
        
    def list_leagues(
        self,
        skip: int = 0, 
        limit: int = 100,
        min_last_changed_date: str = None,
        league_name: str = None
    ) -> List[League]:
        
        """Returns the list of Leagues filterd by parameters 
        
        calls the API v0/leagues endpoint and returns a list of League ojects
        
        Returns :
        A list of schemas.League object. Each represents one SportWorldCenteral fantasy leauge"""


        logger.debug("Entered list leagues")

        params= {
            "skip": skip , 
            "limit": limit, 
            "minimum_last_changed_date": min_last_changed_date, 
            "league_name":  league_name ,}
        
        response= self.call_api(self.LIST_LEAGUES_ENDPOINT, params)
        return [League(**league) for league in response.json()]

        
            


    







