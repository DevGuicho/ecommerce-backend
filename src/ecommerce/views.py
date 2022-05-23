from datetime import datetime
from typing import Tuple
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Order, User, Product, Category
import json
import jwt
import bcrypt
# Create your views here.

secret = 'secreto'


class AuthCheckToken(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        token = data['token']
        try:
            payload = jwt.decode(token, key='secreto', algorithms=['HS256', ])

            users = list(User.objects.filter(id=payload['sub']).values())
            if len(users) > 0:
                user = users[0]
                datos = {'message': 'User logged', 'data': {
                    'email': user['email'],
                    'name': user['name'],
                    'lastname': user['lastname'],
                    'id': user['id']
                }}
            else:
                datos = {'error': 'User not found', 'data': {}}
            return JsonResponse(datos)
        except jwt.InvalidSignatureError as error:
            return JsonResponse({'error': 'Token invalido'})


class AuthLoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        users = list(User.objects.filter(email=data['email']).values())
        if len(users) > 0:
            user = users[0]
            payload_data = {
                "sub": user['id'],
                'email': user['email'],
                'name': user['name'],
                'lastname': user['lastname'],
            }
            if bcrypt.checkpw(bytes(data['password'], 'UTF-8'), bytes(user['password'], 'UTF-8')):
                res = {'message': 'User logged', 'data': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'lastname': user['lastname'],
                    'token': jwt.encode(payload=payload_data, key=secret)}}
            else:
                res = {'error': 'Password not match'}
        else:
            res = {'error': 'User not found'}

        return JsonResponse(res)


class AuthSignUpView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        users = list(User.objects.filter(email=data['email']).values())

        if len(users) > 0:
            return JsonResponse({'error': 'The email is already register'})

        newUser = User.objects.create(
            name=data['name'], lastname=data['lastname'], email=data['email'], password=bcrypt.hashpw(bytes(data['password'], 'UTF-8'), bcrypt.gensalt()).decode('UTF-8'))

        datos = {'message': 'Success'}

        return JsonResponse(datos)


class UserView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if(id > 0):
            users = list(User.objects.filter(id=id).values())
            if len(users) > 0:
                user = users[0]
                datos = {'message': 'User listed',
                         'data': {"email": user.email, "name": user.name, "lastname": user.lastname, "id": id}}
            else:
                datos = {'Message': 'User not found', 'data': {}}
            return JsonResponse(datos)
        else:
            users = list(User.objects.values())
            if len(users) > 0:
                datos = {'message': 'Users Listed', 'data': users}
            else:
                datos = {'message': 'Users Listed', 'data': []}

            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        User.objects.create(
            name=jd['name'], lastname=jd['lastname'], email=jd['email'], password=jd['password'])

        datos = {'message': 'Success'}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        users = list(User.objects.filter(id=id).values())
        if len(users) > 0:
            user = User.objects.get(id=id)
            user.name = jd['name']
            user.lastname = jd['lastname']
            user.email = jd['email']
            user.save()
            datos = {'Message': 'User updated'}

        else:
            datos = {'Message': 'User not found', 'data': {}}

        return JsonResponse(datos)

    def delete(self, request, id):

        users = list(User.objects.filter(id=id).values())
        if len(users) > 0:
            User.objects.filter(id=id).delete()
            datos = {'Message': 'User deleted'}
        else:
            datos = {'Message': 'User not found', 'data': {}}

        return JsonResponse(datos)


class ProductView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if(id > 0):
            products = list(Product.objects.filter(id=id).values())
            if len(products) > 0:
                product = products[0]
                datos = {'message': 'Product listed', 'data': product}
            else:
                datos = {'Message': 'Product not found', 'data': {}}
            return JsonResponse(datos)
        else:
            products = list(Product.objects.values())
            if len(products) > 0:
                datos = {'message': 'Products Listed', 'data': products}
            else:
                datos = {'message': 'Products Listed', 'data': []}

            return JsonResponse(datos)


class CategoryView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if(id > 0):
            categories = list(Category.objects.filter(id=id).values())
            if len(categories) > 0:
                category = categories[0]
                datos = {'message': 'Product listed', 'data': category}
            else:
                datos = {'Message': 'Product not found', 'data': {}}
            return JsonResponse(datos)
        else:
            categories = list(Category.objects.values())
            if len(categories) > 0:
                datos = {'message': 'Categories Listed', 'data': categories}
            else:
                datos = {'message': 'Categories Listed', 'data': []}

            return JsonResponse(datos)


class OrderView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):

        if id > 0:

            orders = Order.objects.filter(user=id)

            data = list()
            for order in orders:
                newOrder = {"id": order.id, "date": order.date,
                            "total_price": order.total_price, "user_id": order.user_id, "products": list(order.products.all().values())}

                data.append(newOrder)

            return JsonResponse({"message": "Orders Listed", "data": data})

    def post(self, request):
        jd = json.loads(request.body)

        try:

            user = User.objects.filter(id=jd['user'])[0]

            newOrder = Order(total_price=jd['total'],
                             user=user, date=datetime.now())
            newOrder.save()
            for product in jd['products']:
                newOrder.products.add(
                    Product.objects.filter(id=product)[0],)

            return JsonResponse({'message': 'successful payment'})
        except:
            return JsonResponse({'error': 'there was an error'})
