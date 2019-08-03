import zeep
import json

wsdl = 'resources/partner.wsdl'
client = zeep.Client(wsdl=wsdl)

'''
login(username: xsd:string, 
password: xsd:string, 
_soapheaders={LoginScopeHeader: ns1:LoginScopeHeader, CallOptions: ns1:CallOptions}) -> result: ns1:LoginResult

ns1:LoginScopeHeader(organizationId: ns1:ID, portalId: ns1:ID)
ns1:CallOptions(client: xsd:string, defaultNamespace: xsd:string)

'''
# read the user data from an untracked file
with open('testdata/users.json', 'r') as f:
    users = json.load(f)

user = users['anzle-dev-ed']

headers = {
    'CallOptions' : {
        'client': 'RestForce/mdapi',
        'defaultNamespace': 'sf'
    }
}

soap_url = 'https://{domain}.salesforce.com/services/Soap/u/{api_version}'.format(domain=user['domain'], api_version=user['apiversion'])

partner = client.create_service(
      '{'+'urn:partner.soap.sforce.com}SoapBinding',
      soap_url
)

login_result = partner.login(username=user['name'], password=user['password']+user['token'], _soapheaders=headers)
# login_result = client.service.login(username=user['name'], password=user['password']+user['token'], _soapheaders=headers)
print(login_result)

session_id = login_result.sessionId
metadata_server_url = login_result.metadataServerUrl

loHeader = {
    'SessionHeader' : {
    'sessionId': login_result.sessionId
    }
}



print(partner.logout(_soapheaders=loHeader))

'''
logout(_soapheaders={SessionHeader: ns1:SessionHeader, CallOptions: ns1:CallOptions})
 -> header: {LimitInfoHeader: ns1:LimitInfoHeader}, body: {}
 ns1:SessionHeader(sessionId: xsd:string)
'''

# print(client.service.logout(_soapheaders={'SessionHeader': login_result.sessionId}))
