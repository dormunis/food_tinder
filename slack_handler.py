import requests

import queries

WEBHOOK_URL = 'https://hooks.slack.com/services/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'

template_rest = "The food train to {rest} is leaving with:\n\t - {users}"


def notify_slack(storage):
    results = storage.get(queries.GET_ALL_GOING)
    parsed_data = _parse_data(results)
    requests.post(WEBHOOK_URL, json=dict(username='FoodAdvisor',
                                         icon_emoji=":fork_and_knife:",
                                         # channel='food_advisor',
                                         text=parsed_data
                                         ))


def _parse_data(data):
    total = [template_rest.format(rest=row['rest_name'], users='\n\t - '.join(list(row['users']))) for row in data]
    return '\n\n'.join(total)


# def register_crontab():
#     import time
#     from subprocess import call
#
#     crontab_path = "/app/crontab"
#     call(["crontab", crontab_path])
#     time.sleep(2)
#     call(["cron"])