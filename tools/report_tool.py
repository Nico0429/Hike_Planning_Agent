
def write_report_as_txt(report_content: str, filename: str = "hike_plan.txt"):
    """
    Writes the final hike planning report to a text file.
    Call this tool ONLY after you have gathered the coordinates and weather.

    :param report_content: The full text of the hiking plan. This MUST include the location, coordinates, weather forecast, and practical recommendations (clothing, water, sunscreen, etc.).
    :param filename: The name of the file to save (e.g., 'crossways_hike.txt').
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(report_content)
        return f"Success! The report has been saved as {filename}."
    except Exception as e:
        return f"Error writing file: {e}"