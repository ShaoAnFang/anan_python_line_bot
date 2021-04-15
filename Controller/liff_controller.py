import os
from flask import request, render_template, Response
from flask_restful import Resource, reqparse

# AIR_ID = os.getenv('LIFF_SHARE_ID')
# AIR_LIFF = f"https://liff.line.me/{AIR_ID}"
LIFF_ID= '1578218509-NWrMdBvk'

class LiffController(Resource):

    def __init__(self, *args, **kwargs):
        # https://www.reddit.com/r/flask/comments/hzbc77/multiple_optional_parameters_in_flaskrestful_api/
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, default='')
        self.reqparse.add_argument('title', type = str, default='')
        self.reqparse.add_argument('cellphone', type = str, default='')
        self.reqparse.add_argument('mail', type = str, default='')
        self.reqparse.add_argument('phone', type = str, default='')
        super().__init__(*args, **kwargs)

    def get(self):
        args = self.reqparse.parse_args()
        if args['name'] is None:
            return Response(render_template('share_message.html', liff_id=LIFF_ID))
        else:
            data_fields = {
                'name': args['name'],
                'title': args['title'],
                'cellphone': args['cellphone'],
                'mail': args['mail'],
                'phone': args['phone'] ,
            }
            # return Response(render_template('share_message.html', flex=msg, liff_id=LIFF_ID))
            return Response(render_template('share_message.html', data=data_fields ,liff_id=LIFF_ID))