from linkedin_v2 import linkedin

# LinkedIn API Credentials
API_KEY = ''
API_SECRET = ''
RETURN_URL = 'http://localhost:8000'

authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, ['r_emailaddress', 'r_liteprofile', 'w_member_social'])
#
# print authentication.authorization_url  # open this url on your browser
# application = linkedin.LinkedInApplication(authentication)


# authentication.authorization_code = 'AQTucAXpJMMzgN90k6QGWFgqlokyFbxd8GQCJZ8xvuIbdqNQLlvFNlMV24ZOrN7U1L25ASNyXApXnARkLNcuC4ZgLFmHGpEiQwg6sIodlA4bDBo9NJB5ls7Yyo4UU2KqVTjXVdB7xxE4CpMNFrolrNF0PLYovrV2bBPmCyQrPt3vdSWzjVWtRJfzuZso5g'
# print authentication.get_access_token()

application = linkedin.LinkedInApplication(token='w8KrvGDp-fnuIGwaqn3TJikyNcL_Q')

# print application.get_connections()