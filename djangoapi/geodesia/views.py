# Create your views here.
from django.http import JsonResponse
from django.views import View
#en lugar de view importaremos esto
#My imports de core
from core.myLib.baseDjangoView import BaseDjangoView #esta clase ya hereda de view

#import de mi app, mis operaciones, donde se encuentran
from geodesia.operations.zonas_trabajo import ZonasTrabajoCrud
from geodesia.operations.rutas_levantamiento import RutasLevantamientoCrud
from geodesia.operations.equipos_geodesicos import EquiposGeodesicosCrud

"""TEORIA DE LA CLASE/ NO ENTRARA EN EL FUNCIONAMIENTO DE LA APP"""
#nombre de la clase que estara enlazada a la url.py, y que se encargara de procesar las peticiones 
class HelloGeodesia(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Geodesia. Hello world. GET METHOD", "data":[request.GET.dict()]})
    
    def post(self, request):
        return JsonResponse({"ok":True,"message": "Geodesia. Hello world. POST METHOD", "data":[request.POST.dict()]})
    
#para insertar un poligono, building/ZONADETRABAJO/  NO ENTRA EN EL FUNCIONAMIETO DE LA APP
class ZonasTrabajo(View):
    #aqui metere las cuatro operaciones insertar, seleccionar y actualizar, borrar para las Zonas de Trabajo
    def post(self, request): #insertar
        d = request.POST.dict()
        return JsonResponse({"ok":True, "message":"Datos recibidos", "data":[request.POST.dict()]})
    
#CRUD DE INSERTAR
class ZonasTrabajoInsert(View):
    #aqui metere las cuatro operaciones insertar, seleccionar y actualizar, borrar para las Zonas de Trabajo
    def post(self, request): #insertar
        d = request.POST.dict()

        crud = ZonasTrabajoCrud()  #creo una instancia de la clase ZonasTrabajoCrud
        r = crud.insert(d)   #hago la operacion insert y le paso el diccionario d con los datos
        
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion insert

class ZonasTrabajoDelete(View):
    #aqui metere las cuatro operaciones insertar, seleccionar y actualizar, borrar para las Zonas de Trabajo
    def post(self, request): #insertar
        d = request.POST.dict()

        crud = ZonasTrabajoCrud()  #creo una instancia de la clase ZonasTrabajoCrud
        r = crud.delete(d)   #hago la operacion delete y le paso el diccionario d con los datos
        
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion delete

"""FIN DE LA TEORIA DE LA CLASE/ NO ENTRARA EN EL FUNCIONAMIENTO DE LA APP"""

"""FUNCIONAMIENTO DE LA APP ---> CLASES PARA PROCESAR LAS PETICIONES DE LA APP"""
#definimos aqui la clase para identificar accion e id
class ZonasTrabajoView(BaseDjangoView): #en lugar de view colocaremos un nuevo import, lo reemplazaremos por baseDjangoView   
    #GET OPERATIONS
    def selectone(self, id):
        #como vemos tiene el id, entonces neustro diccionario solo tendra el id
        #d que es el diccionario que se le pasara a la clase crud, con el id para que sepa que registro tiene que seleccionar
        d = {'id': id} #creo un diccionario con el id para pas
        crud = ZonasTrabajoCrud()  #creo una instancia de la clase ZonasTrabajoCrud
        r = crud.selectAsDicts(d)   #hago la operacion select y le paso el diccionario d con los datos
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion selectone
        
    def selectall(self):
        crud = ZonasTrabajoCrud()
        r = crud.selectAll() #usamos crud antes porque debemos de utilizar un objeto de la clase Zonas, ya que si lo pasamos directomente no podremos acceder a sus metodos, al ser un metodo de instancia y no de clase
        return JsonResponse(r)
        #return JsonResponse({'ok':True, 'message': 'Method selectall called: GET', 'data': []}, status=200)

    #POST OPERATIONS
    def insert(self, request):
        d = request.POST.dict()

        crud = ZonasTrabajoCrud()  #creo una instancia de la clase ZonasTrabajoCrud
        r = crud.insert(d)   #hago la operacion insert y le paso el diccionario d con los datos
        
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion insert
    
    def update(self, request, id):
        d = request.POST.dict()
        #d["id"] = id #agrego el id al diccionario para que la clase crud sepa que registro tiene que actualizar, ya que el id no viene en el body de la peticion, sino en la url, entonces lo agrego al diccionario para pasarselo a la clase crud
        crud = ZonasTrabajoCrud()  
        r = crud.update(d)   

        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion update



        #return JsonResponse({'ok':True, 'message': 'Method update called: POST', 'data': []}, status=200)
    
    def delete(self, id):
    #el delete recibe el id
        d = {'id': id} #creo un diccionario con el id para pasarselo a la clase crud
        crud = ZonasTrabajoCrud()  #creo una instancia de la clase ZonasTrabajoCrud
        r = crud.delete(d)   #hago la operacion delete y le paso el diccionario d con los datos
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion delete


#replicar para mis 2 funciones adicionales de puntos y lineas y enlazarlas a postman
#PARA LINEAS
class RutasLevantamientoView(BaseDjangoView): #en lugar de view colocaremos un nuevo import, lo reemplazaremos por baseDjangoView   
    #GET OPERATIONS
    def selectone(self, id):
        #como vemos tiene el id, entonces neustro diccionario solo tendra el id
        #d que es el diccionario que se le pasara a la clase crud, con el id para que sepa que registro tiene que seleccionar
        d = {'id': id} #creo un diccionario con el id para pas
        crud = RutasLevantamientoCrud()  #creo una instancia de la clase RutasLevantamientoCrud
        r = crud.selectAsDicts(d)   #hago la operacion select y le paso el diccionario d con los datos
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion selectone
        
    def selectall(self):
        crud = RutasLevantamientoCrud()
        r = crud.selectAll() #usamos crud antes porque debemos de utilizar un objeto de la clase Zonas, ya que si lo pasamos directomente no podremos acceder a sus metodos, al ser un metodo de instancia y no de clase
        return JsonResponse(r)
        #return JsonResponse({'ok':True, 'message': 'Method selectall called: GET', 'data': []}, status=200)

    #POST OPERATIONS
    def insert(self, request):
        d = request.POST.dict()

        crud = RutasLevantamientoCrud()  #creo una instancia de la clase RutasLevantamientoCrud
        r = crud.insert(d)   #hago la operacion insert y le paso el diccionario d con los datos
        
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion insert
    
    def update(self, request, id):
        d = request.POST.dict()
        #d["id"] = id #agrego el id al diccionario para que la clase crud sepa que registro tiene que actualizar, ya que el id no viene en el body de la peticion, sino en la url, entonces lo agrego al diccionario para pasarselo a la clase crud
        crud = RutasLevantamientoCrud()  
        r = crud.update(d)   

        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion update



        #return JsonResponse({'ok':True, 'message': 'Method update called: POST', 'data': []}, status=200)
    
    def delete(self, id):
    #el delete recibe el id
        d = {'id': id} #creo un diccionario con el id para pasarselo a la clase crud
        crud = RutasLevantamientoCrud()  #creo una instancia de la clase RutasLevantamientoCrud
        r = crud.delete(d)   #hago la operacion delete y le paso el diccionario d con los datos
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion delete

#PARA PUNTOS
class EquiposGeodesicosView(BaseDjangoView): #importamos las funciones crud de rutas levantamiento
    def selectone(self, id):
        #como vemos tiene el id, entonces neustro diccionario solo tendra el id
        #d que es el diccionario que se le pasara a la clase crud, con el id para que sepa que registro tiene que seleccionar
        d = {'id': id} #creo un diccionario con el id para pas
        crud = EquiposGeodesicosCrud()  #creo una instancia de la clase ZonasTrabajoCrud
        r = crud.selectAsDicts(d)   #hago la operacion select y le paso el diccionario d con los datos
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion selectone
        
    def selectall(self):
        crud = EquiposGeodesicosCrud()
        r = crud.selectAll() #usamos crud antes porque debemos de utilizar un objeto de la clase Zonas, ya que si lo pasamos directomente no podremos acceder a sus metodos, al ser un metodo de instancia y no de clase
        return JsonResponse(r)
        #return JsonResponse({'ok':True, 'message': 'Method selectall called: GET', 'data': []}, status=200)

    #POST OPERATIONS
    def insert(self, request):
        d = request.POST.dict()

        crud = EquiposGeodesicosCrud() 
        r = crud.insert(d)   #hago la operacion insert y le paso el diccionario d con los datos
        
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion insert
    
    def update(self, request, id):
        d = request.POST.dict()
        #d["id"] = id #agrego el id al diccionario para que la clase crud sepa que registro tiene que actualizar, ya que el id no viene en el body de la peticion, sino en la url, entonces lo agrego al diccionario para pasarselo a la clase crud
        crud = EquiposGeodesicosCrud()  
        r = crud.update(d)   

        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion update



        #return JsonResponse({'ok':True, 'message': 'Method update called: POST', 'data': []}, status=200)
    
    def delete(self, id):
    #el delete recibe el id
        d = {'id': id} #creo un diccionario con el id para pasarselo a la clase crud
        crud = EquiposGeodesicosCrud()  #creo una instancia de la clase EquiposGeodesicosCrud
        r = crud.delete(d)   #hago la operacion delete y le paso el diccionario d con los datos
        return JsonResponse(r) #aqui pondre que devuelva la respuesta de la operacion delete

