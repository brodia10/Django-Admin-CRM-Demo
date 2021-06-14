import csv
from django.core.management.base import BaseCommand
from email_tool.models import Customer


class Command(BaseCommand):
    help = "Import a CSV of customer data"

    def add_arguments(self, parser):
        parser.add_argument("csv_file_path", type=str, help="Path to the CSV file to import.")

    def handle(self, *args, **options):
        with open(options["csv_file_path"], newline="") as csvfile:
            successes, failures = 0, 0

            csv_reader = csv.reader(csvfile, delimiter=",")
            for row in csv_reader:
                try:
                    customer = Customer.objects.create(
                        source=row[1],
                        company=row[2],
                        role=row[10],
                        first_name=row[9],
                        last_name=row[8],
                        email=row[11],
                        phone=row[7],
                        address=row[3],
                        city=row[4],
                        state=row[5],
                        zip_code=row[6],
                        website=row[14],
                    )
                    successes += 1
                    self.stdout.write(f'Imported customer "{customer.id}" | ' + self.style.SUCCESS("Success"))
                except Exception:
                    self.stdout.write("Imported customer FAILED!")
                    failures += 1

            self.stdout.write(f"Complete. {successes} successful, {failures} failed.")
