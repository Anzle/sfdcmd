import zeep
import json

class PartnerApi(object):
    DEFAULT_API_VERSION = 46.0
    

    def __init__(self, username=None, password=None, token=None, domain=None, api=DEFAULT_API_VERSION, client=None, namespace=None, sessionid=None):
        '''
            the Init will do the log in based on the provided params and set and return the session id. Need to also return the metadata URL
            for use with the metadata api later on
        '''
        wsdl = 'resources/partner.wsdl'
        partner_client = zeep.Client(wsdl=wsdl)
        
        self.username = username
        self.password = password
        self.token = token
        self.domain = domain
        self.api = api
        self.client = client
        self.namespace = namespace
        
        self.soap_url = 'https://{domain}.salesforce.com/services/Soap/u/{api}'.format(domain=domain, api=api)

        self.partner = partner_client.create_service(
            '{'+'urn:partner.soap.sforce.com}SoapBinding',
            self.soap_url
        )

        self.header = {
            'CallOptions' : {
                'client': client,
                'defaultNamespace': namespace
            }
        }

    def logout(self):
        self.partner.logout(_soapheaders=self.header)
        print('User Logged Out')
    
    def invalidateSessions(self, sessions):
        if sessions != None:
            self.partner.invalidateSessions(sessionIds=sessions, _soapheaders=self.header)
            print('Logged out of given sessions')
        else:
            print('No Sessions provided')
