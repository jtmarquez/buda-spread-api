# SPREAD API
- La solución propuesta está compuesta por dos grandes partes, cada uno con su propio container de Docker:
    1. API(`app/api`):
        a. Se encarga de disponibilizar todos los endpoints necesarios, al igual que implementar la lógica de negocio y persistencia de datos. En este caso, se exponen 4 endpoints relevantes:
            - GET /api/spreads: Permite obtener todos los spreads en una sola llamada
            - GET /api/spreads/{id}: Permite obtener el spread asociado a solamente un Market
            - GET /api/spread-alerts/{id}: Permite obtener un spread guardado, al igual que el spread actual
            - POST /api/spread-alerts: Permite crear un spread guardado
        b. Implementa un websocket que recibe información sobre los cambios en los mercados desde el websocket implementado en la segunda parte de la solución.

    2. Websocket(`app/workers/book_ticks`): Hace una solicitud inicial a la API de Buda para obtener los mercados disponibles, y luego se suscribe al websocket con sus canales asociados. En cada mensaje recibido en el websocket, se envía un mensaje al websocket de la API, el cual se encarga de actualizar la información de los spreads en la base de datos.
- La solución propuesta se encuentra implementada en Python, utilizando FastAPI, SQLite, Peewee, Websockets, entre otros. Se dividió en dos containers de Docker, uno para la API y otro para el websocket, lo que permite escalabilidad, en el caso de ser necesario. Una vez que se inicia el container de la API, el container del websocket se inicia automáticamente, comunicandose internamente a través de una red de Docker.
- Se optó por este camino, pues existian algunas limitantes, como la cantidad de requests permitidas a la API de Buda, la necesidad de contar con información lo más actualizada posible, entre otros.

# Cómo ejecutar la solución
1. Clonar el repositorio
2. Contruir las imágenes de Docker:
    ```bash
    docker-compose build
    ```
3. Iniciar los containers:
    ```bash
    docker-compose up
    ```
4. Listo! La API se encuentra disponible en http://localhost:8001. Para acceder a la **documentación de la API, se puede acceder a http://localhost:8001/api/docs**.


## API:

- A nivel general, se optó por una lógica de routes-controllers-servicios, en donde las routes enrutan las peticiones a los controllers, los cuales se encargan de procesar la información y llamar a los servicios, en caso de ser necesario.
- En cuanto a los servicios, se implementaron 4 modelos en la base de datos (SQLite):
    1. Market: Representa un mercado
    2. MarketBid: Representa un bid de un mercado en particular del libro de ordenes
    3. MarketAsk: Representa un ask de un mercado en particular del libro de ordenes
    4. UserSpread: Representa un spread guardado de usuarios
  Sumado a eso, se agregó dos servicios adicionales:
    1. MarketTick: Solamente define los tipos de ticks que se pueden recibir (Ask o Bid)
    2. MarketSpread: "Modelo virtual" que funciona como integrador y facilitador entre MarketAsks y MarketBids
- Al mismo tiempo, se implementaron 3 controllers:
    1. MarketTick: Recibe los mensajes del websocket y actualiza la información de los bids y asks en la base de datos
    2. Spread: Se encarga de procesar las peticiones relacionadas con obtener los spreads de los mercados
    3. UserSpreadAlert: Se encarga de procesar las peticiones relacionadas a los spreads guardados por los usuarios

## Websocket:
- Se implementó un websocket que se encarga de recibir los mensajes de los mercados y enviarlos a la API, para que esta actualice la información de los spreads en la base de datos. En concreto, se realiza una primera llamada a la API de Buda para obtener los mercados disponibles, y luego con esos datos, se suscribe al websocket con los canales asociados a los mercados.
- Cuando se recibe un mensaje, se envia un mensaje al websocket de la API, el cual se encarga de actualizar la información de los spreads en la base de datos. Es importante mencionar que se reutiliza una misma conexión para ambos websockets, lo que permite una comunicación más eficiente entre ambos.

## Tests
- En la API se implementó solamente tests para los controladores, los cuales se encuentran en la carpeta `tests`
- En el websocket, se implementó tests para los websockets, los cuales se encuentran en `workers/book_ticks/tests`

## Requerimientos cumplidos:
- [x] Necesitamos calcular el spread (explicado más abajo) de cualquiera de los mercados de Buda.com.
- [x] Necesitamos obtener el spread de todos los mercados en una sola llamada.
- [x] Necesitamos guardar un spread de “alerta” el cual en el futuro consultaremos por medio de [polling](https://es.wikipedia.org/wiki/Polling) si el spread actual es mayor o menor de ese spread guardado. Además, debes habilitar un endpoint para que realicemos este polling.


## Esperados
- [x] Que incluyas test automatizados
- [?] Que funcione correctamente según lo especificado
- [?] No es necesario que incluya una interfaz gráfica o persistencia de datos
- [?] Que el código que escribas sea de buena calidad, entendible y mantenible
- [?] Puedes hacer los supuestos que necesites, mientras lo dejes documentado.

## Deseables:
- [x] Que la tarea funcione en un ambiente contenerizado (Docker o similar)
- [x] Documentación de la API