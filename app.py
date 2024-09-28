import json
from datetime import datetime, timedelta

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def count_completed_trainings(data):
    training_counts = {}
    for person in data:
        for completion in person['completions']:
            training_name = completion['name']
            if training_name not in training_counts:
                training_counts[training_name] = 0
            training_counts[training_name] += 1
    return training_counts

def completed_trainings_in_fiscal_year(data, trainings, fiscal_year):
    start_date = datetime(fiscal_year - 1, 7, 1)
    end_date = datetime(fiscal_year, 6, 30)
    result = {}

    for person in data:
        person_name = person['name']
        for completion in person['completions']:
            training_name = completion['name']
            if training_name in trainings:
                completion_date = datetime.strptime(completion['timestamp'], '%m/%d/%Y')
                if start_date <= completion_date <= end_date:
                    if training_name not in result:
                        result[training_name] = []
                    result[training_name].append(person_name)
    return result

def find_expiring_or_expired_trainings(data, check_date):
    result = {}
    check_date = datetime.strptime(check_date, '%m/%d/%Y')
    one_month_after = check_date + timedelta(days=30)

    for person in data:
        person_name = person['name']
        for completion in person['completions']:
            if completion['expires']:
                expiration_date = datetime.strptime(completion['expires'], '%m/%d/%Y')
                if expiration_date < check_date:
                    status = 'expired'
                elif check_date <= expiration_date <= one_month_after:
                    status = 'expires soon'
                else:
                    continue
                if person_name not in result:
                    result[person_name] = []
                result[person_name].append({
                    'training': completion['name'],
                    'expires': completion['expires'],
                    'status': status
                })
    return result

def save_json(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    # Load data
    file_path =  "training.txt" # Update this path
    data = load_data(file_path)

    # Task 1: Count completed trainings
    training_counts = count_completed_trainings(data)
    save_json(training_counts, 'training_counts.json')

    # Task 2: Completed trainings in fiscal year
    trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
    fiscal_year = 2024
    fiscal_year_completions = completed_trainings_in_fiscal_year(data, trainings, fiscal_year)
    save_json(fiscal_year_completions, 'fiscal_year_completions.json')

    # Task 3: Expiring or expired trainings
    check_date = '10/01/2023'
    expiring_or_expired = find_expiring_or_expired_trainings(data, check_date)
    save_json(expiring_or_expired, 'expiring_or_expired.json')

if __name__ == '__main__':
    main()
