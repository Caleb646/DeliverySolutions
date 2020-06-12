


db_collections = ["Users", "MetaData", "AllInv"] #each users' username will be a collection as well

roles_routes = {"admin":("/admin/home",), "user": ("/user/home",),
 "super_employee":("/super_employee/home",), "employee": ("/employee/home",)} #each role with their corresponding homepage

meta_keys = ["meta_id", "db_data", "shipment_num",
 "tag_num", "designer", "user_id", "editable_fields", "storage_price"]

userinv_keys = ["_id", "shipment_num", "designer", "client", "volume",
 "date_entered", "image_num", "description", "location",
  "storage_fees", "paid_last"]

user_keys = ["_id", "username", "password", "roles", "email", "client"]

SEARCH_KEY = "search_method"

NULLVALUE = ("EMPTY", None)
