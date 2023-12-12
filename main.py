import csv
import os
import sys
import urllib.parse


def has_subdomain(url: str) -> bool:
    """
    Returns True if the url has a subdomain. Otherwise, returns False.
    """
    parsed_url = urllib.parse.urlparse(url)
    if not parsed_url.netloc:
        print("Invalid url: {}".format(url))
    if parsed_url.netloc.startswith('www.'):
        parsed_url = parsed_url._replace(netloc=parsed_url.netloc[4:])
    if parsed_url.netloc.count('.') > 1:
        return True
    return False


def transform(file: str) -> None:
    """
    The first column of the csv file is a url. This function removes any row that has a url with a subdomain.
    Examples of urls that should be removed:
      https://investors.usecology.com/~/media/Files/U/US-Ecology-IR-V2/events-pdfs/2019/project-rooster-ir-presentation.pdf
      https://nrcwaplan.usecology.com/Account/LoginForm/6305

    Examples of urls that should be kept:
      https://www.usecology.com/article/us-ecology-inc-acquires-esh-dallas-llc
      https://usecology.com/
    """
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        valid_url_rows = []
        for row in reader:
            # skip the header row
            if row[0] == 'Equity Analysis URL':
                continue
            url = row[0]
            if not has_subdomain(url):
                # print("Valid url: {}".format(url))
                valid_url_rows.append(row)

    # write the valid urls to a new csv file
    with open('valid_urls.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for url_row in valid_url_rows:
            writer.writerow(url_row)

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

    # write the new urls to the same csv file
    with open('valid_urls.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        done = []
        for url_row in new_url_rows:
            # if there is a duplicate row, skip it
            if url_row[0] in done or url_row[0] + '/' in done or url_row[0][:-1] in done:
                continue
            if not url_row[5].startswith('http'):
                print("Invalid url: {}".format(url_row))
                continue
            writer.writerow([url_row[0], url_row[5], '301', 'en'])
            done.append(url_row[0])


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file>")
        sys.exit(1)
    file = sys.argv[1]
    if not os.path.isfile(file):
        print("Invalid file: {}".format(file))
        sys.exit(1)
    transform(file)


if __name__ == '__main__':
    transform("data.csv")
