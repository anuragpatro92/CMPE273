import string

from flask import Flask, request, jsonify, Response,send_file
from sqlitedict import SqliteDict
import json
import  random
import qrcode
import jsonpickle
import base64

from Bookmark import Bookmark
app = Flask(__name__)


@app.route("/api/bookmarks/<id>",methods=['GET'])
def get_Bookmarks(id):
    with SqliteDict('./db.sqlite') as mydict:  # note no autocommit=True
        if id not in mydict.keys():
            print('invalid id recived')


            return Response(status = 404)
        else :
            val = mydict[id]
            val.etag += 1
            mydict[id] = val
            mydict.commit()
            print('updating the count values of the api')

            response = {'id':id,'description':val.description,'name':val.name,'url':val.url}
            print('***Response***')
            print(json.dumps(response))
            return Response(response=json.dumps(response),status=200)


@app.route("/api/bookmarks",methods = ['POST'])
def create_Bookmarks():
    with SqliteDict('./db.sqlite') as mydict:

        if request.method == 'POST':
            dict = request.get_json()

            for key in mydict:
                if(mydict[key].url == dict['url']):
                    response = {'reason':'The given URL already existed in the system.'}
                    print('***Response***')
                    print(json.dumps(response))

                    return Response(response=json.dumps(response),status=400) # returning the response if url exits



            id = get_random_alphanumeric_string(3,3)
            while(id in mydict.keys()):
                id = get_random_alphanumeric_string(3,3)

            mydict[id] = Bookmark(dict['name'],dict['url'],dict['description'])
            mydict.commit()

            response = {'id': id}
            print('***Response***')

            print(json.dumps(response))
        return Response(response=json.dumps(response),status=201)

@app.route("/api/bookmarks/<id>/qrcode",methods = ['GET'])
def get_qrcode(id):
    with SqliteDict('./db.sqlite') as mydict:

        if request.method == 'GET':

            if id not in mydict:
                print('***Response***')
                response = {'message': 'invalid Id'}
                print(json.dumps(response))
                return Response(response=json.dumps(response), status=400, content_type='Application/json')

            data = mydict[id]
            img = qrcode.make(data.url)
            img.save('qr.png')


        return send_file('qr.png', mimetype='image/png')


@app.route("/api/bookmarks/<id>/stats",methods = ['GET','HEADER'])
def get_Stats(id):
    with SqliteDict('./db.sqlite') as mydict:

       if request.method == 'GET' :

           if (id not in mydict.keys()):
               print('***Response***')
               response = {'message': 'invalid Id'}
               print(json.dumps(response))
               return Response(response=json.dumps(response),status=400,content_type='Application/json')


           etag = request.headers.get('ETag')
           bookmark = mydict[id]

           print('current etag = ',type(bookmark.etag))
           print('request etag = ',type(etag))

           if (etag == None) :
               print('etag not in header')
               response = Response(response={str(bookmark.etag)}, status=200, headers={'ETag': bookmark.etag})
               return response
           elif not etag.isnumeric():
               response = {'message': 'invalid request'}
               return Response(response=json.dumps(response), status=400)

           elif int(etag) == bookmark.etag:
               print('etag not modified')
               response = Response(status=304)
               response.headers['etag'] = bookmark.etag
               return Response(status=304,headers={'Etag':bookmark.etag})
           elif int(etag) != bookmark.etag:
               response = Response(response={str(bookmark.etag)}, status=200, headers={'ETag': bookmark.etag})
               return response
           else:
               response = {'message': 'invalid request'}
               return Response(response=json.dumps(response),status=400)

@app.route("/api/bookmarks/<id>",methods = ['DELETE'])
def delete_bookmark(id):
    with SqliteDict('./db.sqlite') as mydict:

        if request.method == 'DELETE':
            if id not in mydict:
                print('***Response***')
                response = {'message': 'invalid Id'}
                print(json.dumps(response))
                return Response(response=json.dumps(response), status=400, content_type='Application/json')



            del mydict[id]
            mydict.commit()
            return Response(status=204)


def get_random_alphanumeric_string(letters_count, digits_count):
    sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))

    sample_list = list(sample_str)
    random.shuffle(sample_list)
    final_string = ''.join(sample_list)
    return final_string