from dataclasses import field, Field, fields
from typing import get_type_hints

from wired import ServiceRegistry, ServiceContainer


def process_request(registry: ServiceRegistry, url_value: str) -> str:
    """ Given URL (customer name), make a Request to handle interaction """

    from .models import View, Url

    # Make the container that this request gets processed in
    container = registry.create_container()

    # Put the url into the container
    url = Url(value=url_value)
    container.register_singleton(url, Url)

    # Create a View to generate the greeting
    view = container.get(View)

    # Generate a response
    response = view()

    return response


def injector_construction(container: ServiceContainer, target):
    """ Introspect dataclass and get arguments from container """

    from .models import Resource, Url, Settings

    if target in (Url, Settings):
        # Don't need to construct this one from a dataclass,
        # it's a singleton the container
        instance = container.get(target)
        return instance

    # Make the args dict that we will construct dataclass with
    args = {}

    # Get the context from the container
    context: Resource = container.get(Resource)

    # Iterate through the dataclass fields
    # Because fields() gives a string for the type, instead of the
    # actual type, let's get a mapping of field name -> field type
    fields_mapping = {f.name: f for f in fields(target)}

    # Now we can iterate over the fields using type hints
    for field_name, field_type in get_type_hints(target).items():

        # Do some special cases first
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
            injected_attr = injected_info['attr']
            injected_type = injected_info['type_']
            # Ask the registry for one of these
            injected_target = container.get(injected_type, context=context)
            # Get the specified attribute off that instance
            field_value = getattr(injected_target, injected_attr)
            args[field_name] = field_value
            continue

        # Now the general case, something like url: Url
        try:
            field_value = container.get(field_type, context=context)
            args[field_name] = field_value
        except TypeError:
            # Seems that wired, when looking up str, gives:
            #  TypeError: can't set attributes of built-in/extension type 'str'
            # We will use that to our advantage to look for a dataclass
            # field default value.
            field_default = getattr(full_field, 'default', None)
            if field_default:
                args[field_name] = field_default
                continue
            else:
                raise LookupError()
        except LookupError:
            # Give up and work around ``wired`` unhelpful exception
            # by adding some context information.
            msg = f'Injector failed for {field_name} on {target.__name__}'
            raise LookupError(msg)

    # Now construct an instance of the target dataclass
    return target(**args)


def register_dataclass(
    registry: ServiceRegistry, target, for_=None, context=None
):
    """ Generic injectory factory for dataclasses """

    # Note: This function could be a decorator which already knows
    # the registry, has all the targets, and can do them in one
    # container that it makes. For example:
    # from wired.decorators import factory
    # @factory(for_=Greeter, context=FrenchCustomer)
    # @datclass
    # class FrenchGreeter(Greeter):
    #   pass

    # The common case, for default registrations we can omit
    # the "for_" as it is the same as the class implementing it
    if for_ is None:
        for_ = target

    if getattr(target, 'factory', None):
        # This class wants to control its factory, use that one
        dataclass_factory = target.factory
    else:
        # Use a generic dataclass factory
        def dataclass_factory(c: ServiceContainer):
            instance = injector_construction(c, target)
            return instance

    registry.register_factory(dataclass_factory, for_, context=context)


def get_injected_value(field_metadata, source):
    """ First try for attr, then key, then call, else source """

    # We can have different flavors of the injected() field type:
    # injected(Breadcrumbs, attr='title')
    # injected(Breadcrumbs, key='title')
    # injected(Breadcrumbs) where Breadcrumbs.__call__ exists
    # injected(Breadcrumbs) where Breadcrumbs.__call__ does not exist

    if 'attr' in field_metadata:
        return getattr(source, field_metadata['attr'], None)
    elif 'key' in field_metadata:
        target_key = field_metadata['key']
        return source[target_key]
    elif field_metadata['call'] is True:
        # field.metadata['injected'] should have one of attr, key, or
        # call. The first two aren't there, so call should be. See if
        # it is true and return the call.
        return source()

    # Otherwise, return the injectable/adapter, same as not having a field
    return source


class InjectedArgumentException(Exception):
    def __init__(self):
        msg = 'Cannot supply both attr and key arguments to inject'
        super().__init__(msg)


def injected(type_, **kwargs) -> Field:
    """ Get a value from an injected type

    We frequently want part of an injectable or adapter. Just an attribute
    or, for injectable/adapters that are dict-like, a key.

    This field type accepts an injectable/adapter and serves three purposes:

    - Get an attribute off of it by passing in attr='somevalue'

    - Or, get a key out of it by passing in key=''

    - Or, if the injectable/adapter has a __call__, return the value
      of callling it

    - Otherwise, return the injectable/adapter, same as if you didn't
      provide a field

     We could just manually do ``injected`` then pick apart the injected
     value. But that exposes a big surface area. This field type lets us
     zero in on what we want.
     """

    # First a sanity check, can't have both attr and key
    if 'attr' in kwargs and 'key' in kwargs:
        raise InjectedArgumentException()

    # If metadata was also passed in, preserve it, otherwise start clean
    if 'metadata' not in kwargs:
        kwargs['metadata'] = {}

    # Let's go in precedence
    if 'attr' in kwargs:
        kwargs['metadata']['injected'] = dict(type_=type_, attr=kwargs['attr'])
        del kwargs['attr']
    elif 'key' in kwargs:
        kwargs['metadata']['injected'] = dict(type_=type_, key=kwargs['key'])
        del kwargs['key']
    elif 'call' in kwargs:
        # We'll presume that it is call=True
        kwargs['metadata']['injected'] = dict(type_=type_, call=kwargs['call'])
        del kwargs['call']
    else:
        # Default is to treat call=True if nothing else provided
        kwargs['metadata']['injected'] = dict(type_=type_, call=True)

    return field(**kwargs)
