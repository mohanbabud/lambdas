import json
import os


def getAlarms(event_stream, stats, filters):
    if 'Records' not in event_stream:
        return [event_stream]

    events = []
    for event in event_stream['Records']:
        alarm = event.get('Sns')
        if alarm is None:
            continue

        message = alarm.get('Message')
        if message is None:
            continue

        alarm = json.loads(message)
        if 'Message' in alarm:
            alarm = alarm['Message']

            # Apply filtering based on multiple filters
            include_event = True
            for filter_type, filter_value in filters.items():
                if alarm.get(filter_type) == filter_value:
                    include_event = False
                    stats['suppressed'] += 1  # Increment suppressed count
                    break

            if include_event:
                events.append(alarm)

    return events


def sup_filters():
    filters = {}
    allowed_filters = ['source', 'summary', 'aws_account', 'ci_arn']
    filters_count = int(os.environ.get('FILTERS_COUNT', 0))
    if filters_count > 0:
        for i in range(1, filters_count + 1):
            filter_type = os.environ.get(f'FILTER_TYPE_{i}')
            filter_value = os.environ.get(f'FILTER_VALUE_{i}')
            if filter_type and filter_value:
                filters[filter_type] = filter_value
    return filters


def lambda_handler(event, context):
    stats = dict(received=0, queued=0, suppressed=0)  # Initialize suppressed count
    filters = sup_filters()
    for alarm in getAlarms(event, stats, filters):
        stats['received'] += 1
