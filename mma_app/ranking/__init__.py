"""
Package initialization for MyApp.

This is the core package for MyApp, providing the initial setup, configuration,
and metadata information about the application.

Owner: Ali Zarreh @zarreh.ai
Created Date: YYYY-MM-DD
Last Modified Date: YYYY-MM-DD
Version: 1.0.0
"""

# Standard library imports
import os
import logging

# Third-party imports
# e.g., import flask

# Local application imports
# from .module1 import Class1
# from .module2 import function2

# Application metadata
__app_name__ = "MMA_ranking"
__author__ = "Ali Zarreh"
__created_date__ = "2020-01-01"
__last_modified_date__ = "2024-04-01"
__version__ = "1.0.0"
__license__ = ""

# Initialize logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_app(config):
    """
    Initialize the application with the given configuration.

    Parameters:
    - config: A configuration dictionary or object.
    """
    logger.info(f"Initializing {__app_name__} v{__version__} with provided configuration.")

# Optionally, any global configurations or variables can be set here
APP_CONFIG = {
    'setting1': 'value1',
    'setting2': 'value2',
}

# Initialize the app if specific conditions are met (optional)
if os.getenv('MYAPP_ENV') == 'production':
    initialize_app(APP_CONFIG)
