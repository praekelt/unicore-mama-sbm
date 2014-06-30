import os
import csv


class CsvImporter(object):
    def __init__(self, num_days):
        self.num_days = num_days

    def read_rows_from_csv_file(self, csvfile_name):
        if not os.path.exists(csvfile_name):
            raise Exception('File does not exist: %s' % csvfile_name)

        with open(csvfile_name, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Only process rows that actually have data
                if any([column for column in row]):
                    yield row

    def import_csv(self, file_path):
        return self.build_messages(self.read_rows_from_csv_file(file_path))

    def build_messages(self, rows):
        days = dict()

        for row in rows:
            week = int(row['week'].strip())
            text = row['text'].strip().decode('utf-8')

            current_day = 0
            if not days.get(current_day):
                days[current_day] = dict()

            while current_day <= self.num_days - 1 and days.get(current_day).get(week):
                current_day += 1
                if not days.get(current_day):
                    days[current_day] = dict()

            if not days.get(current_day).get(week):
                days.get(current_day)[week] = text
            else:
                # last row per week get concatenated
                # if messages wer
                days.get(current_day)[week] += ' ' + text

        return days
