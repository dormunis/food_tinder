from schema import Schema, Optional

interest_schema = Schema({
    'user_id': basestring,
    'rest_id': basestring,
    Optional('going'): bool
})

