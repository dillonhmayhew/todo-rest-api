from sqlalchemy.inspection import inspect


class Serializer(object):
    """Class to serialize db.model objects in a way they can be jsonified."""

    def serialize(self):
        '''Return a dict key/value pairs for each key in the object.'''
        return {k: getattr(self, k) for k in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        '''Return a list of dictionaries created by Serializer.serialize().'''
        return [k.serialize() for k in l]