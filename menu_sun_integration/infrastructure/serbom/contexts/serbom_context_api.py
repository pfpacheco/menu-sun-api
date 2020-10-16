import os

import requests
from menu_sun_integration.infrastructure.context.context_api import ContextAPI


class SerbomContextAPI(ContextAPI):
    def __init__(self):
        super().__init__(os.getenv('URL_SEPARATION_SERBOM'))
        self.token = os.getenv('SERBOM_TOKEN')
        self.url_header = os.getenv('SOAPACTION_SERBOM')

    def parser(self, response):
        return response.text

    def authentication(self) -> str:
        return """<?xml version="1.0" encoding="utf-8"?>
         <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
           <soap:Body>
             <Separacao xmlns="http://ws.serbom.com.br:5763/wsserbom_hom/">
               <oWsAcessoModel>
                 <StrId>menupontocom</StrId>
                 <StrToken>%s</StrToken>
               </oWsAcessoModel>
               <ListWsSeparacaoModel>
                 %s
               </ListWsSeparacaoModel>
             </Separacao>
           </soap:Body>
         </soap:Envelope>  
         """

    def __bind_url(self):
        self.url = self.base_url

    def do_post(self, request):
        self.__bind_url()

        xml_post = self.authentication() % (self.token, request.payload)
        header = {'Content-Type': 'text/xml; charset=utf-8',
                  "SOAPAction": self.url_header}

        self._logger.info(key="serbom_context_api", description=f'request_payload(url="{request.resource}")',
                          payload=self._logger.dumps(xml_post))
        return requests.post(url=self.base_url, data=xml_post.encode('utf-8'), headers=header)

    def do_get(self, request):
        raise NotImplementedError
