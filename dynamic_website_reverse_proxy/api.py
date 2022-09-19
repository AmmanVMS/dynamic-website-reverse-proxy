"""The API that is provided by the JSON endpoint.
"""
from http import HTTPStatus
from .full_website import FullWebsite

class APIv1:
    """This represents the API version 1"""

    def __init__(self, database, config):
        """Serve the database with a configuration through the API."""
        self._db = database
        self._config = config

    def create_website(self, user, data):
        """Create a website as a user with certain data in it."""
        website = FullWebsite(data["source"], data["domain"], self._config)
        website.change_owner_to(user)
        self._db.add_website(website)
        return {
            "status": HTTPStatus.CREATED,
            "data": {
                "type": "website",
                "source": data["source"],
                "domain": data["domain"],
                "owner" : user.id
            }
        }
