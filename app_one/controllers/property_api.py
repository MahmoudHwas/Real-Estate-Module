import json

from odoo import http
from odoo.http import request
class PropertyApi(http.Controller):
    @http.route("/v1/property", methods=['POST'], type='http' ,auth="none", csrf=False)
    def post_property(self):
        try:
            args = request.httprequest.data.decode()
            val = json.loads(args)
            if not val.get("name"):
                return request.make_json_response({
                    "message": "name is required"
                }, status=400)
            res = request.env['property'].sudo().create(val)
            if res:
                return request.make_json_response({
                    "message": "Property has been created successfully"
                }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": error
            }, status=400)
    @http.route("/v1/property/json", methods=['POST'], type='json', auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        val = json.loads(args)
        res = request.env['property'].sudo().create(val)
        if res:
            return [{
                "message": "Property has been created successfully"
            }]

    @http.route("/v1/property/<int:property_id>", methods=['PUT'], type='http', auth="none", csrf=False)
    def update_property(self, property_id):
        property_id = request.env['property'].sudo().search([('id', '=', property_id)])
        args = request.httprequest.data.decode()
        val = json.loads(args)
        property_id.write(val)
        print(property_id.garden_area)

    @http.route("/v1/property/<int:property_id>", method=['GET'], type='http', auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_rec = request.env['property'].sudo().search([('id', '=', property_id)], limit=1)
            if not property_rec:
                return request.make_json_response({
                    "message": "not found"
                }, status=400)

            return request.make_json_response({
                "id": property_rec.id,
                "name": property_rec.name,
            })
        except Exception as error:
            return request.make_json_response({
                "message": str(error)
            }, status=400)

    @http.route("/v1/property/<int:property_id>", method=['DELETE'], type='http', auth="none", csrf=False)
    def unlink_property(self, property_id):
        try:

            property_rec = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_rec:
                return request.make_json_response({
                    "message": "not found"
                }, status=400)

            property_rec.unlink()
            return request.make_json_response({
                "message" : "property has beed deleted successfully"
            })
        except Exception as error:
            return request.make_json_response({
                "message": error
            }, status=400)