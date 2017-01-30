'''
Validation of fields that are present is done in the individual forms.
However, as it is possible to skip lots of steps we want to be able
to validate the presence of a value for those required fields before
we publish.
'''
from collections import OrderedDict

REQUIRED_FIELDS = [
    ('title', 'You must provide a title'),
    ('summary', 'You must provide a summary'),
    ('organisation', 'You must choose an organisation'),
    ('licence', 'You must choose a licence'),
    ('frequency', 'You must choose an update frequency')
]

def check_required_fields(dataset):
    errors = OrderedDict({})
    for f, label in REQUIRED_FIELDS:
        if not getattr(dataset, f):
            errors[f] = label

    return errors
