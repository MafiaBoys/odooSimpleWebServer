# other: mafiaboys


import xmlrpc.client as xmlrpclib
from functools import partial
from termcolor import colored ,cprint
from sys import exit

databases = {
  'default': {

    'URI': 'http://localhost:8069/',
    'database': 'database',
    'username':'admin',
    'password':'password'
  }
}
class XmlrpcClient(object):

  __attributes__  = ['URI','database','username','password']

  def __init__(self ,databases=databases ,attribute='default'):
    super(XmlrpcClient, self).__init__()

    if self.hasAttributes(databases ,[attribute]):
       this = databases[attribute]
       if not self.hasAttributes(databases[attribute] ,self.__attributes__): 
          self.reportError('databases not has Attributes') 
       _user = this['username']
    else:
        self.reportError('databases not attribute <{attr}>'.format(attr=attribute))

    _pass = this['password']
    URI = self.addLinkURI(this['URI'] ,'xmlrpc/2')
    commonURI = self.addLinkURI(URI ,'common')
    common = xmlrpclib.ServerProxy (commonURI)

    try:
       UID = common.login(this['database'] ,_user ,_pass)
    except Exception as e:
        self.reportError("Server Error")

 
    objectURI = self.addLinkURI(URI,'object')

    self.execute_command = partial(xmlrpclib.ServerProxy(
                objectURI).execute,this['database'] ,
                UID,
                _pass)

  def search(self,model_id ,domain=[],*args):
      resu = None
      try:
        resu = self.execute_command(model_id ,'search' ,domain ,*args)
      except xmlrpclib.Fault as e:
          self.reportError('?') 
      return resu

  def read(self,model_id ,domain=[],*args):
      _read = None
      try:
        _read = self.execute_command(model_id ,'search_read' ,domain ,*args)
      except xmlrpclib.Fault as e:
          self.reportError('read()') 
      return _read

  def write(self,model_id ,ids=[],fields={}):
      _write = None
      try:
        _write = self.execute_command(model_id ,'write' ,ids ,fields)
      except xmlrpclib.Fault as e:
          self.reportError(xmlrpclib.dumps(e)) 
      return _write

  def checkPermissions(self,model_id,permissions=[],raise_exception=False):
      _permission = False
      try: 
         _permission = self.execute_command(model_id,'check_access_rights',
         [permissions],{'raise_exception':raise_exception})
         
      except xmlrpclib.Fault as e:
          self.reportError('checkPermissions()')   
      return _permission


  def hasAttributes(self,_dict,attributes=[]):
      dictAttributeError = True
      if _dict and attributes:
          try:
            for attribute in attributes:
                if not attribute in _dict:
                   dictAttributeError = not dictAttributeError
                   break
          except AttributeError as e:
              return not dictAttributeError

      if dictAttributeError:
         for attribute in attributes:
             if not _dict[attribute]:
                dictAttributeError = not dictAttributeError
                break

      return dictAttributeError  


  def addLinkURI(self,URI ,_subURI , sepURI='/',mode=False):
        
      if _subURI and URI:
         if not _subURI.endswith(sepURI) and mode:
            _subURI += sepURI
                  
         if not URI.endswith(sepURI):
            URI += sepURI

         return URI + _subURI
      return URI

  def reportError(self,messageError=None):
      if messageError:
         print (messageError)
      exit (1)          

if __name__ == '__main__':

# # # # # # # # # # # # # # # # # # # # # # # #  test model ir.module.module

#  serverA = XmlrpcClient(attribute='<tagnameA>')
#  model_id = 'ir.module.module'

#  if serverA.checkPermissions(model_id,['read','write']):
#     records = serverA.read(model_id,[('state','=','installed')])
#     for record in records:
#         print (record['id'],record['name'],record['state'])

# copyLeft @ all rights changed
