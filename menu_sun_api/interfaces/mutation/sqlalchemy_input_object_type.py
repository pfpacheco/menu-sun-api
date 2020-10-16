from sqlalchemy.ext.hybrid import hybrid_property
from menu_sun_api.interfaces.mutation.converter import convert_sqlalchemy_column, \
    convert_sqlalchemy_composite, convert_sqlalchemy_hybrid_method, \
    convert_sqlalchemy_relationship
from collections import OrderedDict
from sqlalchemy.inspection import inspect as sqlalchemyinspect
import graphene
from graphene.types.field import Field
from graphene.types.structures import List
from graphene.types.utils import yank_fields_from_attrs
from graphene.utils.subclass_with_meta import SubclassWithMeta_Meta
from graphene_sqlalchemy.registry import get_global_registry


class SQLAlchemyInputObjectType(graphene.InputObjectType):

    def accept(self, visitor):
        return visitor.visit(self)

    @classmethod
    def __init_subclass_with_meta__(  # pylint: disable=arguments-differ
            cls, model=None, registry=None, only_fields=(), exclude_fields=(),
            optional_fields=(),
            **options
    ):
        if not registry:
            registry = get_global_registry()

        sqla_fields = yank_fields_from_attrs(
            construct_fields(model,
                             registry,
                             only_fields,
                             exclude_fields),
            _as=graphene.Field,
        )

        for key, value in sqla_fields.items():
            if key in optional_fields:
                type_ = value.type if isinstance(
                    value.type, SubclassWithMeta_Meta) else value.type.of_type
                value = type_(
                    description=value.description
                )
            setattr(cls, key, value)

        setattr(cls, "model", model)

        super(SQLAlchemyInputObjectType, cls).__init_subclass_with_meta__(
            **options
        )

    def map(self, additional={}, excludes=[]):
        obj = self.model()
        fields = self.__dict__
        for key, value in fields.items():
            if (key in excludes):
                continue
            class_type = getattr(self.get_type(), key)
            if (key) in self:
                if (isinstance(class_type, Field)):
                    setattr(obj, key, value)
                elif (isinstance(class_type, List)):
                    for i in value:
                        rs = i.map()
                        attr = getattr(obj, key)
                        attr.append(rs)

        for key, value in additional.items():
            setattr(obj, key, value)

        return obj


def construct_fields(model, registry, only_fields, exclude_fields):
    inspected_model = sqlalchemyinspect(model)

    fields = OrderedDict()

    for name, column in inspected_model.columns.items():
        is_not_in_only = only_fields and name not in only_fields
        # is_already_created = name in options.fields
        is_excluded = name in exclude_fields  # or is_already_created
        if is_not_in_only or is_excluded:
            # We skip this field if we specify only_fields and is not
            # in there. Or when we exclude this field in exclude_fields
            continue
        converted_column = convert_sqlalchemy_column(column, registry)
        fields[name] = converted_column

    for name, composite in inspected_model.composites.items():
        is_not_in_only = only_fields and name not in only_fields
        # is_already_created = name in options.fields
        is_excluded = name in exclude_fields  # or is_already_created
        if is_not_in_only or is_excluded:
            # We skip this field if we specify only_fields and is not
            # in there. Or when we exclude this field in exclude_fields
            continue
        converted_composite = convert_sqlalchemy_composite(composite, registry)
        fields[name] = converted_composite

    for hybrid_item in inspected_model.all_orm_descriptors:

        if isinstance(hybrid_item, hybrid_property):
            name = hybrid_item.__name__

            is_not_in_only = only_fields and name not in only_fields
            # is_already_created = name in options.fields
            is_excluded = name in exclude_fields  # or is_already_created

            if is_not_in_only or is_excluded:
                # We skip this field if we specify only_fields and is not
                # in there. Or when we exclude this field in exclude_fields
                continue

            converted_hybrid_property = convert_sqlalchemy_hybrid_method(
                hybrid_item)
            fields[name] = converted_hybrid_property

    # Get all the columns for the relationships on the model
    for relationship in inspected_model.relationships:
        is_not_in_only = only_fields and relationship.key not in only_fields
        # is_already_created = relationship.key in options.fields
        is_excluded = relationship.key in exclude_fields  # or is_already_created
        if is_not_in_only or is_excluded:
            # We skip this field if we specify only_fields and is not
            # in there. Or when we exclude this field in exclude_fields
            continue
        converted_relationship = convert_sqlalchemy_relationship(
            relationship, registry)
        name = relationship.key
        fields[name] = converted_relationship

    return fields
