import json
import os
from jsonschema.validators import validator_for

EVENT_PATH = 'event'
SCHEMA_PATH = 'schema'


def load_json(filepath):
    with open(filepath, encoding='utf-8') as file:
        return json.load(file)


def get_errors_from_eventlog(eventlog):
    errors = []
    if eventlog:
        if eventlog["event"]:
            schema_path = os.path.join(SCHEMA_PATH, eventlog["event"] + '.schema')
            if os.path.exists(schema_path):
                schema_data = load_json(schema_path)
                validator = validator_for(schema_data)(schema_data)
                for error in validator.iter_errors(eventlog):
                    errors.append(error.message)
            else:
                errors.append("Нет файла схемы " + eventlog["event"] + '.schema')
        else:
            errors.append("В логе отсутсвует поле event для проверки по файлу схемы.")
    else:
        errors.append("Файл лога пустой.")
    return errors


if __name__ == '__main__':
    errorslog = {}
    for root, dirs, files in os.walk(EVENT_PATH):
        for file in files:
            eventlog = load_json(os.path.join(EVENT_PATH, file))
            errorslog[file] = get_errors_from_eventlog(eventlog)
            with open("errorslog.txt", "w", encoding='utf-8') as f:
                for log in errorslog:
                    f.write(log + '\n')
                    for error in errorslog[log]:
                        f.write(error + '\n')
                    f.write('\n')
