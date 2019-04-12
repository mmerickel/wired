from dataclasses import dataclass, fields, Field, MISSING
from typing import get_type_hints, Optional, Tuple

from wired import ServiceContainer


class Context:
    """ Marker interface for lookups by request context """
    pass


@dataclass()
class Injector:
    """ Introspect dataclass and get arguments from container """
    container: ServiceContainer

    def __call__(self,
                 target,
                 singletons: Optional[Tuple] = (),
                 ):

        container = self.container

        # Don't need to construct this target from a dataclass,
        # it's a singleton instance already in the container
        if target in singletons:
            instance = container.get(target)
            return instance

        # Make the args dict that we will construct dataclass with
        args = {}

        # Get the context from the container
        context: Context = container.get(Context)

        # Iterate through the dataclass fields
        # Because fields() gives a string for the type, instead of the
        # actual type, let's get a mapping of field name -> field type
        fields_mapping = {f.name: f for f in fields(target)}

        # Iterate through the dataclass fields
        for field_name, field_type in get_type_hints(target).items():

            # Do some special cases first.
            if field_type == ServiceContainer:
                # Doing this style of bailing out quickly for performance
                # reasons. Don't want to keep doing "if", though it
                # means some repeititions.
                args[field_name] = container
                continue

            # See if this field is using the injectable field, e.g.
            # url: str = injected(Url, attr='value')
            full_field: Field = fields_mapping[field_name]
            if full_field.metadata.get('injected', False):
                injected_info = full_field.metadata['injected']
                injected_attr = injected_info.get('attr')
                injected_type = injected_info['type_']
                # Ask the registry for one of these
                injected_target = container.get(injected_type, context=context)

                # If attr is used, get specified attribute off that instance
                if injected_attr:
                    field_value = getattr(injected_target, injected_attr)
                else:
                    field_value = injected_target
                args[field_name] = field_value
                continue

            # Now the general case, something like url: Url
            try:
                field_value = container.get(field_type, context=context)
                args[field_name] = field_value
            except TypeError:
                # Seems that wired, when looking up str, gives:
                #   TypeError: can't set attributes of built-in/extension type 'str'
                # We will use that to our advantage to look for a dataclass
                # field default value.
                field_default = getattr(full_field, 'default', None)
                if field_default is not MISSING:
                    args[field_name] = field_default
                    continue
                else:
                    msg = f'No default value on field {field_name}'
                    raise LookupError(msg)
            except LookupError:
                # Give up and work around ``wired`` unhelpful exception
                # by adding some context information.

                # Note that a dataclass with a ``__post_init__`` might still
                # do some construction. Only do this next part if there's
                # no __post_init__
                if not hasattr(target, '__post_init__'):
                    msg = f'Injector failed for {field_name} on {target.__name__}'
                    raise LookupError(msg)

        # Now construct an instance of the target dataclass
        return target(**args)
