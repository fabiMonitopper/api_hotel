from ast import arguments
from turtle import home
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
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
        return{'hoteis':[hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'Nome' não pode ser em branco")
    argumentos.add_argument('estrelas', type=str, required=True, help="O campo 'Nome' não pode ser em branco")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')


    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404  

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return{"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 
       
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return{'message': 'Aconteceu um erro interno na hora de salvar o Hotel'}, 500
        return hotel.json()
        

    def put(self, hotel_id): 
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.salve_hotel()
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return{'message': 'Aconteceu um erro interno na hora de salvar o Hotel'}, 500
        return hotel.json(), 201

        
    def delete(self, hotel_id): 
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return{'message':'Erro ao deletar o Hotel '}, 500
            return {'message': 'Hotel deleted'}
        return {'messege': 'Hotel not found.'}, 404