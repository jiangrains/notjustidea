# -*- coding: utf-8 -*-
class Utils():
	
    def get_random_string(len):
        return ''.join(random.sample(string.ascii_letters + string.digits, len))

    def get_uuid():
        u = uuid.uuid1()
        return u.hex