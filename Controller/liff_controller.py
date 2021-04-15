import os
from flask import request, render_template, Response
from flask_restful import Resource

# from utils.db import find_site
# from utils.flex import county_flex_template

# AIR_ID = os.getenv('LIFF_SHARE_ID')
# AIR_LIFF = f"https://liff.line.me/{AIR_ID}"
LIFF_ID= '1578218509-NWrMdBvk'



class LiffController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, name, title, cellphone, mail, phone):
        if name is None:
            return Response(render_template('share_message.html', liff_id=LIFF_ID))
        else:
            data_fields = {
                'name': name,
                'title': title,
                'cellphone': cellphone,
                'mail': mail,
                'phone': phone
            }
            # return Response(render_template('share_message.html', flex=msg, liff_id=LIFF_ID))
            return Response(render_template('share_message.html', data=data_fields ,liff_id=LIFF_ID))