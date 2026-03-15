
def write_report_as_txt(report_lines: list[str], filename: str = "hike_plan.txt"):
    """
    Writes the final hike planning report to a text file.
    Call this tool ONLY after you have gathered the coordinates and weather.

    :param report_lines: The full text of the hiking plan, provided as a list of strings. Each paragraph or bullet point should be a separate string in this list.
    :param filename: The name of the file to save (e.g., 'crossways_hike.txt').
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("\n".join(report_lines))
        return f"Success! The report has been saved as {filename}."
    except Exception as e:
        return f"Error writing file: {e}"