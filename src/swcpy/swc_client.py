## minimal sdk , just to call the health check  of the swc api 
import httpx 

class SWCClient:
    def __init__(self, swc_base_url: str):
        self.swc_base_url= swc_base_url 

    def get_health_check(self):
        #make api call
        with httpx.Client(base_url=self.swc_base_url) as client:
            return client.get("/")
        
        