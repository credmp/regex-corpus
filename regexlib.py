from zeep import Client

client = Client("http://regexlib.com/WebServices.asmx?WSDL")
print client.service.ListAllAsXml(maxrows=4)


