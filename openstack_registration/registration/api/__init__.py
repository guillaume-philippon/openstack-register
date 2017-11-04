"""
API is a module that manage REST API for openstack-registration. The following URI can be used with
the API

API URI:

- **/users**: list of users
    - **/users/user_id**: a specific user

- **/groups**: list of groups
    - **/groups/group**: a specific group

API output format supported:

- Json
- HTML

API method supported:

- **GET**: get information
- **PUT**: modify information
- **POST**: create a new entry
- **DELETE**: delete a entry

"""
from registration.api import users
