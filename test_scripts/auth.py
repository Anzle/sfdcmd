import zeep
import json

wsdl = 'resources/partner.wsdl'
client = zeep.Client(wsdl=wsdl)

# read the user data from an untracked file
with open('testdata/users.json', 'r') as f:
    users = json.load(f)

user = users['anzle-dev-ed']

header = {
    'CallOptions' : {
        'client': 'Anzle/sfdcmd',
        'defaultNamespace': 'sf'
    }
}

# setup soap url for access
soap_url = 'https://{domain}.salesforce.com/services/Soap/u/{api_version}'.format(domain=user['domain'], api_version=user['apiversion'])

# create partner client
partner = client.create_service(
      '{'+'urn:partner.soap.sforce.com}SoapBinding',
      soap_url
)

# login
login_result = partner.login(username=user['name'], password=user['password']+user['token'], _soapheaders=header)
print(login_result)

# add the SessionId to the header
header['SessionHeader'] = {
    'sessionId': login_result.sessionId
}

# invalidate sessions
print(partner.invalidateSessions(sessionIds=[login_result.sessionId], _soapheaders=header))

# logout
# print(partner.logout(_soapheaders=header))

