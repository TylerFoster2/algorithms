import csv

class Table:
    def __init__(self, name, columns, rows):
        self.name = name
        self.columns = columns
        self.rows = rows

    def to_table_html(self):
        head = "".join(f"<th>{col}</th>" for col in self.columns)
        body = "\n".join(
            "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
            for row in self.rows
        )
        return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"

def parse_csv(file_path):
    with open(file_path, newline = "") as f:
        reader = csv.reader(f)

        columns = next(reader)

        rows = []
        for row in reader:
            rows.append(row)

    return Table(file_path, columns, rows)

def main():
    csv_path = "algorithms_tracker.csv"
    table = parse_csv(csv_path)

    table_html = table.to_table_html()
    with open("index.html", "r", encoding="utf-8") as f:
        page = f.read()

    page = page.replace("<!-- TABLE_HERE -->", table_html)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(page)

    print("Table inserted into index.html")

if __name__ == "__main__":
    main()