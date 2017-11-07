"""
API is a module that manage REST API for openstack-registration. The following URI can be used with
the API.

API URI:

- uri://**users**: list of users
    - uri://**users/user_id**: a specific user

- uri://**groups**: list of groups
    - uri://**groups/group**: a specific group
        - uri://**groups/group/attribute**: a specific attribute of group

API output format supported:

- Json
- HTML

API method supported:

- **GET**: get information
- **PUT**: modify information
- **POST**: create a new entry
- **DELETE**: delete a entry

"""
from registration.api import users, groups
