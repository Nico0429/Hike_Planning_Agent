import ollama
import tools as t
from tools import TOOL_MAP, get_weather_forecast, get_co_ordinates


MODEL = "qwen2.5:7b"
TOOLS = t.DEFINITIONS

def start_chat():
    print(f"--- Hike Planning Agent Active ({MODEL}) ---")



    #This is the base prompt given to the model
    messages = [{
        'role': 'system',
        'content': (
            "You are a hike planning agent. You are a tour guide that occasionally says some funny things. "
            "You must gather real world information using the tools provided. "
            "Do not make up your own information, only provide what was given by the tools. "
            "Once you have both coordinates and weather, you MUST generate a comprehensive hiking plan and save it using the write_report_as_txt tool. "
            "The generated plan MUST include:\n"
            "- The hike/location identified\n"
            "- The co-ordinates of the start and end points\n"
            "- The weather forecast for the given date\n"
            "- Practical recommendations (clothing, water, sunscreen, wind/rain protection, etc.) based on the predicted weather and location. "
            "\n\nCRITICAL RULE: NEVER guess or make up a date for the weather tool. If the user does not explicitly give you a date, YOU MUST ASK THE USER for the date before calling the weather tool."
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

    start_chat()



