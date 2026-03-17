import ollama
import tools as t
import datetime
from tools import TOOL_MAP, get_weather_forecast, get_co_ordinates, get_trail_points


MODEL = "qwen2.5:7b"
TOOLS = t.DEFINITIONS
DATETIME = datetime.datetime.now()

def start_chat():
    print(f"--- Hike Planning Agent Active ({MODEL}) ---")



    #This is the base prompt given to the model
    messages = [{
        'role': 'system',
        'content': (
            "### TOP PRIORITY RULE: ABSOLUTELY NEVER guess a date for the weather tool. "
            "If the user has not given a specific date (YYYY-MM-DD), you MUST ask them. "
            f"For reference, the current date is {DATETIME}.\n"
            "Do not call 'get_weather_forecast' until the date is confirmed.\n\n"

            "You are a witty English-speaking hike planning agent. You must use tools to get real info.\n\n"

            "### TRAIL SELECTION PROTOCOL:\n"
            "1. Get coordinates for the location.\n"
            "2. Call 'get_trail_points'.\n"
            "3. **CRITICAL**: If multiple trails are returned, you MUST stop and list them for the user. "
            "Ask the user: 'Which trail would you like to plan for?'\n"
            "4. **WAIT** for the user's response. Do NOT analyze the data or write code. Just list the names and ask.\n\n"

            "### REPORTING STRUCTURE:\n"
            "When calling 'write_report_as_txt', you MUST provide 'report_lines' as a list of strings following this exact structure:\n"
            "1. '# HIKING PLAN: [Trail Name]'\n"
            "2. '**Location**: [Area Name, Province]'\n"
            "3. '**Date**: [YYYY-MM-DD]'\n"
            "4. '---\'\n"
            "5. '## 1. TRAIL DETAILS'\n"
            "6. '* **Start Coordinates**: [Latitude, Longitude]'\n"
            "7. '* **End Coordinates**: [Latitude, Longitude]'\n"
            "8. '## 2. WEATHER FORECAST'\n"
            "9. '* **Condition**: [Summary from tool]'\n"
            "10. '* **Temperature**: High of [Max]°C, Low of [Min]°C'\n"
            "11. '## 3. PRACTICAL RECOMMENDATIONS'\n"
            "12. '* [Clothing recommendations]'\n"
            "13. '* [Water and hydration needs]'\n"
            "14. '* [Sun/Rain protection requirements]'\n\n"

            "Once the trail is selected and the date is provided, call 'get_weather_forecast' and then 'write_report_as_txt'."
        )
    }]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']: break

        #This is the user input given to the model
        messages.append({
            'role' : 'user',
            'content' : user_input
        })

        try:

            #This is the initial prompt to the model
            response = ollama.chat(
                model = MODEL,
                messages = messages,
                tools = TOOLS,
                options= {'temperature' : 0.4}
            )

            #Case where a tool is being called
            while response.message.tool_calls:

                messages.append(response.message) #Add response to the message history

                for call in response.message.tool_calls:

                    func_name = call.function.name
                    args = call.function.arguments

                    if func_name in TOOL_MAP:

                        print(f"  [System: Executing {func_name} with {args}]")

                        #Actual tool call
                        result = TOOL_MAP[func_name](**args)

                        #This is now appending the result of the tool to the messages
                        messages.append({
                            'role' : 'tool',
                            'content' : str(result),
                            'name' : func_name
                        })

                    else:
                        print(f"  [System: Tool {func_name} not found in TOOLS]")

                #This is a second call because the Model had to first stop and ask for a tool call,
                #this is now prompting the Model using the results we got from the tool call.
                response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    tools = TOOLS,
                    options={'temperature': 0.1}
                )

            print(f"Adventure Guide: {response.message.content.strip()}")

            messages.append(response.message) #Add response to the message history


        except Exception as e:
            print(f"--- {e}")



if __name__ == '__main__':

    #get_co_ordinates("Crossways, Eastern Cape, South Africa")
    #get_weather_forecast(-33.9015149,25.1754914,"2026-03-20")
    #get_trail_points(-33.9015149,25.1754914,1000)
    start_chat()



