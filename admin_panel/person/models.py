from django.db import models

# Create your models here.
from mongoengine import Document, StringField, ListField, DateTimeField, ObjectIdField, BooleanField, DictField
    
class Users(Document):
    '''
    model for users
    '''
    name = StringField(required=True)
    email = StringField(required=True, unique=False)
    password = StringField(required=True)
    api_keys = ListField(default=[])
    organization_id = ObjectIdField()
    role_id = ObjectIdField()
    adverse_media = BooleanField(default=False)
    open_search = DictField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField(null=True)

    def __init__(self, *args, **kwargs):
        '''
        Custom constructor to handle default values.
        '''
        super(Users, self).__init__(*args, **kwargs)

        # Ensure that 'deleted_at' is set to None if not provided
        if not self.deleted_at:
            self.deleted_at = None