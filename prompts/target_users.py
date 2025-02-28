import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("API_KEY")

def target_users_model(string):
    """ To evaluate how well the product spec explains its target userbase

    Args:
        string (str): section of text extracted from Notion

    Returns:
        str: GPT's evaluation of the input
    """
    try:
        response = openai.Completion.create(
            model = "text-davinci-002",
            prompt = f"The following paragraph is explaining the audience or target userbase of a product specification. Provide a number from a scale of 1-100 that rates how well it answers 'who is this for?'. After providing a score, explain why the score was given and what could potentially be improved upon if anything. You must give the score first and then write several in-depth sentences.\n{string}",
            temperature = 0.2,
            max_tokens = 512,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )
        return response["choices"][0]["text"]
    except Exception as e:
        return f"target_users: {e}" # placeholder for now


# for internal testing

""" TEST_INPUT = "Our solution saves time for internal team members and their peers or supervisors by reducing the number of exchanges needed to iterate and improve their product spec. It also saves time for members of the AI Camp Discord who are looking for feedback on their product spec in the same manner. On a larger scale, anyone writing product specs has this problem, which presents a greater opportunity for us. However, for the MVP, we’re focused on product spec drafting by the AI Camp Internal Team."

print(target_users_model(TEST_INPUT)) """
