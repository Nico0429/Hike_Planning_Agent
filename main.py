import ollama
import tools as t

MODEL = "qwen2.5:3b"
TOOLS = [t.get_co_ordinates,t.get_weather_forecast,t.get_weather_forecast]
NAMES_TO_FUNCS = {f.__name__: f for f in TOOLS}


def start_chat():
    print(f"--- Hike Planning Agent Active ({MODEL}) ---")

    #This is the base prompt given to the model
    messages = [{
        'role' : 'system',
        'content' : (
            "You are a hike planning agent. You are a tour guide that occasionally says some funny things"
            "You must gather real world information using the tools provided."
            "Do not make up your own information, only provide what was given by the tools"
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

            response = ollama.chat(
                model = MODEL,
                messages = messages,
                tools = TOOLS,
                options= {'temperature' : 0.4}
            )

            print(f"Adventure Guide: {response.message.content.strip()}")

        except Exception as e:
            print(f"--- {e}")



if __name__ == '__main__':
    start_chat()



