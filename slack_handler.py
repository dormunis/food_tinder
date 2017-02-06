import requests

import queries

WEBHOOK_URL= 'https://hooks.slack.com/services/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'

template_rest = "The food train to {rest} is leaving with:\n{names}"


def notify_slack(storage):
    results = storage.get(queries.GET_ALL_GOING)
    parsed_data = _parse_data(results)
    requests.post(WEBHOOK_URL, data=dict(text=parsed_data))


def _parse_data(data):
    total = [template_rest.format(rest=row['rest_name'], users='\n\t'.join(list(row['users']))) for row in data]
    return '\n\n'.join(total)
