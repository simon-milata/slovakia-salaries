import logging


def process_stats(data_dict: str) -> dict:
    data_dict["salary ranges"] = remove_hourly_salary_ranges(data_dict["salary ranges"])
    data_dict["salary ranges"] = calculate_salary_ranges(data_dict["salary ranges"])

    print(data_dict["salary ranges"])


def remove_hourly_salary_ranges(stats_salary_dict: dict) -> dict:
    result_dict = {}
    for key, value in stats_salary_dict.items():
        try:
            pay = key.replace("from", "").replace("eur", "").replace(" ", "").strip()
            pay = int(pay)
        except (ValueError, TypeError) as e:
            logging.error(f"Converting key {pay} to int failed. Error: {e}")
            raise

        if pay < 100:
            continue

        result_dict[pay] = value
    return result_dict


def calculate_salary_ranges(salary_data_dict: dict) -> dict:
    result_dict = {}

    sorted_salary_list = sorted(salary_data_dict.items())


    for i in range(len(sorted_salary_list) - 1):
        current_salary, current_data = sorted_salary_list[i]
        next_salary, next_data = sorted_salary_list[i + 1]

        salary_range = f"{current_salary} - {next_salary}"
        salary_range_count = current_data["count"] - next_data["count"]

        result_dict[salary_range] = salary_range_count

    last_salary, last_data = sorted_salary_list[-1]

    result_dict[f"{last_salary}+"] = last_data["count"]

    return result_dict
