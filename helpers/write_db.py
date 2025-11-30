def write_records(path: str, rows: list[str]):
    with open(path, "w", encoding="utf-8") as file:
        for row in rows:
            if not row.endswith("\n"):
                row += "\n"
            file.write(row)
