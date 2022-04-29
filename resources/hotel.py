from ast import arguments
from turtle import home
from flask_restful import Resource, reqparse
hoteis = [
    {
        'hotel_id': 'apha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria' : 420.34,
        'cidade' : 'são paulo' 

    },
        {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria' : 380.34,
        'cidade' : 'rio de janeiro'

    },
        {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria' : 320.34,
        'cidade' : 'santa catarina'

    },
]

class Hoteis(Resource):
    def get(self):
        return{'hoteis':hoteis}

class Hotel(Resource):
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found'}, 404  

    def post(self, hotel_id): 
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('nome')
        argumentos.add_argument('estrelas')
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')

        dados = argumentos.parse_args()

        novo_hotel = {
            'hotel_id' : hotel_id,
            'nome' : dados['nome'],
            'estrelas': dados['estrelas'],
            'diaria': dados['diaria'],
            'cidade': dados['cidade']
        }

        hoteis.append(novo_hotel)
        return novo_hotel, 200



    def put(self, hotel_id): 
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        


    def delete(self): 
        pass