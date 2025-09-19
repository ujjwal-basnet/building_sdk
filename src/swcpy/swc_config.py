import os 
from dotenv import load_dotenv
load_dotenv() 

import os

class SWCConfig:
    def __init__(
        self,
        swc_base_url: str = None,
        backoff: bool = True,
        backoff_max_time: int = 30,
        bulk_file_format: str = "csv",
    ):
        """
        Constructor for configuration class.
        Contains initialization values to overwrite defaults.

        Args:
            swc_base_url (optional): Base URL for API calls. Pass this in
                or set in environment variable SWC_API_BASE_URL.
            backoff: Whether SDK should retry calls with backoff on errors.
            backoff_max_time: Max seconds to keep retrying a failed call.
            bulk_file_format: Format for bulk files, 'csv' or 'parquet'.
        """
        self.swc_base_url = swc_base_url or os.getenv("SWC_API_BASE_URL")
        print(f"SWC_API_BASE_URL in SWCConfig init: {self.swc_base_url}")
        if not self.swc_base_url:
            raise ValueError(
                "Base URL is required. Set SWC_API_BASE_URL environment variable."
            )
        self.swc_backoff = backoff
        self.swc_backoff_max_time = backoff_max_time
        self.swc_bulk_file_format = bulk_file_format

    def __str__(self):
        """Return string representation of config object for logging"""
        return (
            f"Base URL: {self.swc_base_url}, "
            f"Backoff: {self.swc_backoff}, "
            f"Max Backoff Time: {self.swc_backoff_max_time}, "
            f"Bulk File Format: {self.swc_bulk_file_format}"
        )

