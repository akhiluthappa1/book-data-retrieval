import json
from django.http import JsonResponse
from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import xml.dom.minidom
from rest_framework.decorators import api_view
import xml.etree.ElementTree as ET



@csrf_exempt
@api_view(["GET"])
def get_book_details(request):
    response = {}
    book_url = request.GET.get('book_url')
    params = {'key': config('KEY')}
    r = requests.get(url=book_url, params=params)
    # print("result", r._content.decode())
    f = open("test.xml", "w+")
    f.write(r._content.decode())
    f.close()
    tree = ET.parse('test.xml')
    root = tree.getroot()
    # print("root", root[1][26][1][1].text)
    response['title'] = root[1][1].text
    response['average_rating'] = root[1][18].text
    response['ratings_count'] = root[1][17][5].text
    response['num_pages'] = root[1][19].text
    response['image_url'] = root[1][8].text
    response['publication_year'] = root[1][10].text
    authors = ''
    i=1
    for author in root[1][26]:
        if author[1].text:
            print("AUTHOR", author[1].text)
            if authors:
                authors = authors + ', ' + author[1].text
            else:
                authors = authors + author[1].text
            i = i+1
    response['authors'] = authors
    return JsonResponse(response, status=200, safe=False)












