import csv
import html
import os
import re


class Table:
    def __init__(self, name, columns, rows):
        self.name = name
        self.columns = columns
        self.rows = rows

    def to_table_html(self, link_column="Algorithm", link_map=None):
        if link_map is None:
            link_map = {}

        head = "".join(f"<th>{html.escape(col)}</th>" for col in self.columns)
        body_rows = []
        for row in self.rows:
            cells = []
            for col, cell in zip(self.columns, row):
                text = html.escape(str(cell))
                if col == link_column and cell in link_map:
                    href = html.escape(link_map[cell])
                    cells.append(f"<td><a href=\"{href}\">{text}</a></td>")
                else:
                    cells.append(f"<td>{text}</td>")
            body_rows.append("<tr>" + "".join(cells) + "</tr>")

        body = "\n".join(body_rows)
        return f"<div class=\"card\"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def parse_csv(file_path):
    with open(file_path, newline="") as f:
        reader = csv.reader(f)

        columns = next(reader)

        rows = []
        for row in reader:
            rows.append(row)

    return Table(file_path, columns, rows)


def slugify(text):
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "item"


def write_detail_pages(table, output_dir="pages"):
    os.makedirs(output_dir, exist_ok=True)
    link_map = {}
    used = {}

    for row in table.rows:
        row_dict = dict(zip(table.columns, row))
        title = row_dict.get("Algorithm", "Algorithm")
        base = slugify(title)
        count = used.get(base, 0) + 1
        used[base] = count
        slug = f"{base}-{count}" if count > 1 else base
        filename = f"{slug}.html"
        link_map[title] = f"{output_dir}/{filename}"

        fields = "\n".join(
            f"<li><strong>{html.escape(k)}:</strong> {html.escape(v)}</li>"
            for k, v in row_dict.items()
        )

        page_html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    .card {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 16px; }}
  </style>
</head>
<body>
  <a href=\"../index.html\">&larr; Back</a>
  <h1>{html.escape(title)}</h1>
  <div class=\"card\">
    <ul>
      {fields}
    </ul>
  </div>
</body>
</html>"""

        out_path = os.path.join(output_dir, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)

    return link_map


def main():
    csv_path = "algorithms_tracker.csv"
    table = parse_csv(csv_path)

    link_map = write_detail_pages(table)
    table_html = table.to_table_html(link_map=link_map)
    with open("index.html", "r", encoding="utf-8") as f:
        page = f.read()

    marker_start = "<!-- TABLE_START -->"
    marker_end = "<!-- TABLE_END -->"

    if marker_start in page and marker_end in page:
        before = page.split(marker_start)[0]
        after = page.split(marker_end)[1]
        page = f"{before}{marker_start}\n{table_html}\n{marker_end}{after}"
    elif "<!-- TABLE_HERE -->" in page:
        page = page.replace("<!-- TABLE_HERE -->", f"{marker_start}\n{table_html}\n{marker_end}")
    else:
        insert_block = f"{marker_start}\n{table_html}\n{marker_end}"
        if "</body>" in page:
            page = page.replace("</body>", f"{insert_block}\n</body>")
        else:
            page = page + "\n" + insert_block

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(page)

    print("Table inserted into index.html")


if __name__ == "__main__":
    main()