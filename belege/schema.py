# from drf_spectacular.extensions import OpenApiFilterExtension


# well this does not work

# class LookupChoiceFilterExtension(OpenApiFilterExtension):
#     target_class = "django_filters.rest_framework.LookupChoiceFilter"

#     def get_schema_operation_parameters(self, auto_schema, *args, **kwargs):
#         print(f"✨ Called LookupChoiceFilterExtension for {self.target}")
#         field = self.target.field_name
#         model_field = getattr(
#             getattr(self.target, "model", None)._meta, "get_field", lambda x: None
#         )(field)
#         description = model_field.help_text if model_field else ""

#         params = []
#         for lookup, label_suffix in self.target.lookup_choices:
#             param_name = f"{field}__{lookup}"
#             params.append(
#                 {
#                     "name": param_name,
#                     "required": False,
#                     "in": "query",
#                     "schema": {
#                         "type": "string",
#                     },
#                     "description": f"{label_suffix} — {description}",
#                 }
#             )
#         return params
