from blist import sortedset
from datetime import datetime
from dateutil.tz import tzutc
from uuid import UUID


class Field(object):
    BASE_TYPE = None

    def __init__(self, columnname=None, default=None):
        self.columnname = columnname

        # validate default type is appropriate for field
        if default is not None and not isinstance(default, self.BASE_TYPE):
            raise Exception("Property %s must be an instance of %s" % (
                self.columnname, self.BASE_TYPE
            ))
        self.default = default

    def __get__(self, instance, objtype):
        value = instance._data.get(self.columnname)
        if value is not None:
            return value
        return self.default

    def __set__(self, instance, value):
        instance._data[self.columnname] = value


class BooleanField(Field):
    BASE_TYPE = bool

    def __set__(self, instance, value):
        if value is None:
            instance._data[self.columnname] = None
            return
        if not isinstance(value, self.BASE_TYPE):
            raise Exception("Property %s must be an instance of bool" % (
                self.columnname
            ))

        instance._data[self.columnname] = value


class DateTimeField(Field):
    BASE_TYPE = datetime

    def __get__(self, instance, objtype):
        if not instance._data.get(self.columnname):
            return None
        return instance._data[self.columnname]

    def __set__(self, instance, value):
        if value and not isinstance(value, self.BASE_TYPE):
            raise Exception("Property %s must be an instance of datetime" % (
                self.columnname
            ))
        if value:
            instance._data[self.columnname] = value.replace(tzinfo=tzutc())
        else:
            instance._data[self.columnname] = None


class IntegerField(Field):
    BASE_TYPE = int

    def __set__(self, instance, value):
        if value is None:
            instance._data[self.columnname] = None
            return
        if not isinstance(value, self.BASE_TYPE):
            raise Exception("Property %s must be an instance of int" % (
                self.columnname
            ))

        instance._data[self.columnname] = value


class FloatField(Field):
    BASE_TYPE = float

    def __set__(self, instance, value):
        if value is None:
            instance._data[self.columnname] = None
            return
        if not isinstance(value, self.BASE_TYPE):
            raise Exception("Property %s must be an instance of float" % (
                self.columnname
            ))

        instance._data[self.columnname] = value


class StringField(Field):
    BASE_TYPE = basestring

    def __set__(self, instance, value):
        if value and not isinstance(value, self.BASE_TYPE):
            raise Exception("Property %s must be an instance of basestring" % (
                self.columnname
            ))
        instance._data[self.columnname] = value


class MapField(Field):
    BASE_TYPE = dict

    def __set__(self, instance, value):
        if value and not isinstance(value, self.BASE_TYPE):
            raise Exception("Property %s must be an instance of dict" % (
                self.columnname
            ))

        if value is None:  # explicit check for None
            instance._data[self.columnname] = dict()
            return

        instance._data[self.columnname] = value

    def __get__(self, instance, objtype):
        if instance._data.get(self.columnname) is None:  # explicit None check
            if self.default:
                instance._data[self.columnname] = self.default
            else:
                instance._data[self.columnname] = dict()
        return instance._data[self.columnname]


class SetField(Field):
    BASE_TYPE = set

    def __set__(self, instance, value):
        if value and not (isinstance(value, set) or
                          isinstance(value, sortedset)):
            raise Exception("Property %s must be an instance of set or "
                            "sortedset" % (self.columnname))

        if value is None:  # explicit check for None
            instance._data[self.columnname] = set()
            return

        instance._data[self.columnname] = value

    def __get__(self, instance, objtype):
        if instance._data.get(self.columnname) is None:  # explicit None check
            if self.default:
                instance._data[self.columnname] = self.default
            else:
                instance._data[self.columnname] = set()
        return instance._data[self.columnname]


class UuidField(Field):
    BASE_TYPE = UUID

    def __set__(self, instance, value):
        if value is None:
            instance._data[self.columnname] = None
            return
        if not isinstance(value, self.BASE_TYPE):
            raise Exception("Property %s must be an instance of int" % (
                self.columnname
            ))

        instance._data[self.columnname] = value

    def __get__(self, instance, objtype):
        if instance._data.get(self.columnname) is None:  # explicit None check
            if self.default:
                instance._data[self.columnname] = self.default
            else:
                instance._data[self.columnname] = None
        return instance._data[self.columnname]


class ModelMeta(type):

    _registry = {}

    def __new__(cls, name, bases, attrs):
        if name not in cls._registry:
            cls._registry[name] = {}
        for attrname, field_obj in attrs.items():
            if isinstance(field_obj, Field):
                # use name of attribute if there is no columnname
                if not field_obj.columnname:
                    field_obj.columnname = attrname
                cls._registry[name][attrname] = field_obj
        return super(ModelMeta, cls).__new__(cls, name, bases, attrs)


class Model(object):
    __metaclass__ = ModelMeta

    def __init__(self, data=None):
        self._data = {}

        if not data:
            return

        attributes = self.attributes

        for key, value in data.iteritems():
            if key not in attributes:
                raise Exception("Invalid attribute %s" % key)
            setattr(self, key, value)

    def __repr__(self):
        str = "<%s " % self.__class__.__name__
        pairs = []
        for attr in self.attributes:
            if not attr.startswith("_"):
                pairs.append("%s=%s" % (attr, repr(getattr(self, attr))))
        str += ' '.join(pairs)
        str += ">"
        return str

    @property
    def attributes(self):
        """ returns list of attributes registered on the model """
        return sorted(ModelMeta._registry[self.__class__.__name__])

    def attrnames_and_columnnames(self):
        """ returns mapping dict where the key is the attribute name on
        the object, and the value is the database columnname """
        r = ModelMeta._registry[self.__class__.__name__]
        mapping = {}
        for attrname, fieldobj in r.iteritems():
            mapping[attrname] = fieldobj.columnname
        return mapping

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        for attr in self.attributes:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        return {
            attr: getattr(self, attr) for attr in self.attributes
        }
