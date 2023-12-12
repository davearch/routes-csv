import csv
import os
import sys
import urllib.parse


class URLProcessor:
    @staticmethod
    def has_subdomain(url: str) -> bool:
        """
        Returns True if the URL has a subdomain. Otherwise, returns False.
        """
        parsed_url = urllib.parse.urlparse(url)
        if not parsed_url.netloc:
            print(f"Invalid URL: {url}")
            return False
        if parsed_url.netloc.startswith('www.'):
            parsed_url = parsed_url._replace(netloc=parsed_url.netloc[4:])
        return parsed_url.netloc.count('.') > 1

    def transform_urls(self, file: str) -> None:
        """
        Processes the CSV file to remove rows with URLs having a subdomain.
        Also, replaces full URLs with relative paths.
        """
        self._process_file(file)
        self._replace_with_relative_urls()

    def _process_file(self, file: str) -> None:
        # ... [Code for processing the CSV file] ...
        # Return two lists: one for valid URLs and one for new URLs
        with open(file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            valid_url_rows = []
            for row in reader:
                # skip the header row
                if row[0] == 'Equity Analysis URL':
                    continue
                url = row[0]
                if not self.has_subdomain(url):
                    valid_url_rows.append(row)
        self._write_to_csv('valid_urls.csv', valid_url_rows)

    @staticmethod
    def _write_to_csv(file: str, data: list) -> None:
        # ... [Code to write data to a CSV file] ...
        # Write the valid urls to a new csv file
        with open(file, 'w') as csv_file:
            done = []
            writer = csv.writer(csv_file)
            for url_row in data:
                # if there is a duplicate row, skip it
                if url_row[0] in done or url_row[0] + '/' in done or url_row[0][:-1] in done:
                    continue
                url = url_row[1] if len(url_row) < 5 else url_row[5]
                if not url.startswith('http'):
                    print("Invalid url: {}".format(url_row))
                    continue
                writer.writerow([url_row[0], url, '301', 'en'])
                done.append(url_row[0])

    def _replace_with_relative_urls(self) -> None:
        # ... [Code to replace full URLs with relative paths] ...
        # go through the valid urls and replace them with a relative url with only the path.
        # Write the new urls to the same csv file.
        with open('valid_urls.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            new_url_rows = []
            for row in reader:
                url = row[0]
                parsed_url = urllib.parse.urlparse(url)
                new_url = parsed_url.path
                row[0] = new_url
                new_url_rows.append(row)
        self._write_to_csv('valid_urls.csv', new_url_rows)


class Application:
    def __init__(self, file: str):
        self.file = file
        self.url_processor = URLProcessor()

    def run(self):
        if not os.path.isfile(self.file):
            print(f"Invalid file: {self.file}")
            sys.exit(1)
        self.url_processor.transform_urls(self.file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <file>")
        sys.exit(1)

    app = Application(sys.argv[1])
    app.run()
