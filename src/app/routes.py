from app import render_template, request, Response
from app import app, api
from app import Resource, swag_from
from app import db
from app.mainform import MainForm
from app.models import Node
import re


@app.route('/')
def get():
    form = MainForm()
    return render_template('index.html', title='Sign In', form=form)


class UserApiGetRender(Resource):
    @swag_from('static/swag/render.yml')
    def get(self):
        ret = [{"id": n.id, "parent": n.parent, "text": n.text} for n in Node.query.all()]
        return ret


class UserApiAdd(Resource):
    @swag_from('static/swag/add_root.yml')
    def post(self):
        if request.json['text'] == '':
            return Response(status=400)
        unique = True
        for n in Node.query.filter_by(parent='#').all():
            if n.text == request.json['text']:
                unique = False
        if unique & bool(re.fullmatch(r'(?:\w+\s?)+\S', request.json['text'])):
            u = Node(parent='#', text=request.json['text'])
            db.session.add(u)
            db.session.commit()
        return Response(status=201)


class UserApi(Resource):
    @swag_from('static/swag/post.yml')
    def post(self):
        if (request.json['id'] == '') | (request.json['text'] == ''):
            return Response(status=400)
        unique = True
        for n in Node.query.filter_by(parent=request.json['id']).all():
            if n.text == request.json['text']:
                unique = False
        if unique & bool(re.fullmatch(r'(?:\w+\s?)+\S', request.json['text'])):
            u = Node(parent=request.json['id'], text=request.json['text'])
            db.session.add(u)
            db.session.commit()
        return Response(status=201)

    @swag_from('static/swag/put.yml')
    def put(self):
        if (request.json['id'] == '') | (request.json['text'] == ''):
            return Response(status=400)
        unique = True
        for n in Node.query.filter_by(parent=Node.query.get(request.json['id']).parent).all():
            if n.text == request.json['text']:
                unique = False
        if unique & bool(re.fullmatch(r'(?:\w+\s?)+\S', request.json['text'])):
            u = Node(id=request.json['id'], parent=Node.query.get(request.json['id']).parent, text=request.json['text'])
            db.session.delete(Node.query.get(request.json['id']))
            db.session.commit()
            db.session.add(u)
            db.session.commit()
        return Response(status=204)

    @swag_from('static/swag/delete.yml')
    def delete(self):
        if request.json['id'] == '':
            return Response(status=400)
        del_len = 1
        new_del_len = 1
        for_del = {Node.query.get(request.json['id'])}
        while (True):
            for n in for_del.copy():
                for_del.update(set(Node.query.filter_by(parent=n.id).all()))
            new_del_len = len(for_del)
            if new_del_len == del_len:
                break
            else:
                del_len = new_del_len
        for n in for_del:
            db.session.delete(n)
        db.session.commit()
        return Response(status=204)


api.add_resource(UserApi, '/nodes', endpoint='node')
api.add_resource(UserApiAdd, '/add', endpoint='add')
api.add_resource(UserApiGetRender, '/render', endpoint='render')
