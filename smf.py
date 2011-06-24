# -*- coding: utf-8 -*-

import hashlib
from string import lower
from django.db import connection
from django.contrib.auth.models import User

class ModelBackend(object):


    def authenticate(self, username=None, password=None):
        valid = False
        email = None
        
        if not (username is None) and not (password is None):
            
            encoded = username.encode('utf-8', 'ignore')
            hash = hashlib.sha1(lower(username.encode('utf-8', 'ignore')) + password.encode('utf-8', 'ignore')).hexdigest()
            
            from django.db import connections
            current_connection = connections['smf']
            cursor = current_connection.cursor()
            
            cursor.execute("select member_name, email_address, real_name, avatar from smf_members where member_name = '%s' and passwd = '%s' and is_activated = '1'" % (encoded, hash))
            row = cursor.fetchone()
            
            if row is not None:
                valid = True
            
        if valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.email = row[1]
                user.is_staff = False
                user.is_superuser = False
                user.set_unusable_password() # disable login through Model backend
                user.save()
                
                
                profile = user.get_profile()
                profile.avatar = row[3]
                profile.realname = row[2]
                profile.save()
                
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None