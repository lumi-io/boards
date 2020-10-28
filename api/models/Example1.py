import mongoengine as me


# If the document has nested fields, use EmbeddedDocument to defined the fields of the embedded document and EmbeddedDocumentField to declare it on the parent document.
class NestedExample1(me.EmbeddedDocument):
    field1 = me.StringField()
    field2 = me.DecimalField()
    field3 = me.IntField()


# To declare a model that represents a Mongo document, create a class that inherits from Document and declare each of the fields.
class Example1(me.Document):
    field1 = me.StringField(required=True)
    field2 = me.IntField()
    field3 = me.StringField()
    field4 = me.ListField()
    nestedfield1 = me.EmbeddedDocumentField(NestedExample) # Calling the nested field