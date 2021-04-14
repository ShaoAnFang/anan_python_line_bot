import os
from flask import request, render_template, Response
from flask_restful import Resource

from utils.db import find_site
from utils.flex import county_flex_template

# AIR_ID = os.getenv('LIFF_SHARE_ID')
LIFF_ID= '1578218509-NWrMdBvk'
AIR_LIFF = f"https://liff.line.me/{AIR_ID}"


class LiffController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        return Response(render_template('share_message.html', flex=msg, liff_id=LIFF_ID))