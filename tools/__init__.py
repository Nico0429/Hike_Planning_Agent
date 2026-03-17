from .weather_tool import get_weather_forecast
from .report_tool import write_report_as_txt
from .coordinates_tool import get_co_ordinates
from .trail_points import get_trail_points

TOOL_MAP = {
    "get_weather_forecast": get_weather_forecast,
    "write_report_as_txt" : write_report_as_txt,
    "get_co_ordinates" : get_co_ordinates,
    "get_trail_points": get_trail_points

}

# List of definitions for the LLM to read
DEFINITIONS = [get_weather_forecast, write_report_as_txt, get_co_ordinates,get_trail_points]