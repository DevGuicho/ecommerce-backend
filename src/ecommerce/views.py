from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import User, Product, Category
import json
# Create your views here.


class UserView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if(id > 0):
            users = list(User.objects.filter(id=id).values())
            if len(users) > 0:
                user = users[0]
                datos = {'message': 'User listed', 'data': user}
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
