from schema import Schema, Optional

interest_schema = Schema({
    'user_id': basestring,
    'restaurant_name': basestring,
    Optional('going'): bool
})

