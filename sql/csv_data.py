from csv import DictReader,DictWriter

class CSVData:
    def __init__(self,file_path):
        self.file_path = file_path

    def csv_rows(self):
        with open(self.file_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = DictReader(file)
            for row in csv_reader:
                yield row

    def update_csv(self,header, data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            csv_writer = DictWriter(file, fieldnames=header)
            csv_writer.writeheader()
            for row in data:
                csv_writer.writerow(row)
        
    