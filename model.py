from attr import s
from notion_extraction import extract_product_spec_text, parse_product_spec_text, extract_id_from_url
import requests
#from text.peer import notion_token

# unused labels = ['', '', '', 'Success Criteria', 'Success Metrics', '', '', '', '']
    
# until the backend is implemented

import aiohttp
import asyncio

def get_prompts(parsed_product_spec):

    prompts = []

    label_to_prompt = {
        'Problem Statement' : {
            'prompt' : f"The following paragraph is the problem statement section of a product specification. First, evaluate and respond with a precise score from 1-100 with how well the problem statement has been written. Next, explain why this score was given along with specific feedback on what can be improved. You must give the score first and then write several in-depth sentences.",
            'temperature' : 0.1,
            'max_tokens' : 512,
            'top_p' : 1,
            'frequency_penalty' : 0,
            'presence_penalty' : 0
        },
        'Solution Statement' : {
            'prompt' : f"The following paragraph is the solution statement of a product specification. First, evaluate and respond with a precise score from 1-100 with how well the solution statement has been written. Next, explain why this score was given along with specific feedback on what can be improved. You must give the score first and then write several in-depth sentences.",
            'temperature' : 0.1,
            'max_tokens' : 512,
            'top_p' : 1,
            'frequency_penalty' : 0,
            'presence_penalty' : 0
        },
        'Who Has This Problem?' : {
            'prompt' : f"The following paragraph is explaining the audience or target userbase of a product specification. Provide a number from a scale of 1-100 that rates how well it answers 'who is this for?'. After providing a score, explain why the score was given and what could potentially be improved upon if anything. You must give the score first and then write several in-depth sentences.",
            'temperature' : 0.2,
            'max_tokens' : 512,
            'top_p' : 1,
            'frequency_penalty' : 0,
            'presence_penalty' : 0
        },
        'Milestones' : {
            'prompt' : f"The following paragraph is the milestones section of a product specification. First, evaluate and respond with a precise score from 1-100 with how well the milestones have been written. Next, explain why this score was given along with specific feedback on what can be improved. You must give the score first and then write several in-depth sentences.",
            'temperature' : 0.1,
            'max_tokens' : 512,
            'top_p' : 1,
            'frequency_penalty' : 0,
            'presence_penalty' : 0
        },
        'Schedule of Deliverables' : {
            'prompt' : f"The following paragraph is the schedule section of a product specification. First, evaluate and respond with a precise score from 1-100 with how well the schedule has been written. Next, explain why this score was given along with specific feedback on what can be improved. You must give the score first and then write several in-depth sentences.",
            'temperature' : 0.1,
            'max_tokens' : 512,
            'top_p' : 1,
            'frequency_penalty' : 0,
            'presence_penalty' : 0
        },
        'Tech Stack' : {
            'prompt' : f"The following paragraph is the technology stack section of a product specification. First, evaluate and respond with a precise score from 1-100 with how well the technology stack has been written. Next, explain why this score was given along with specific feedback on what can be improved. You must give the score first and then write several in-depth sentences.",
            'temperature' : 0.2,
            'max_tokens' : 512,
            'top_p' : 1,
            'frequency_penalty' : 0,
            'presence_penalty' : 0
        },
        'Happy Path' : {
            'prompt' : f"The following paragraph is the happy path section of a product specification. First, evaluate and respond with a precise score from 1-100 with how well the happy path has been written. Next, explain why this score was given along with specific feedback on what can be improved. You must give the score first and then write several in-depth sentences.",
            'temperature' : 0.1,
            'max_tokens' : 512,
            'top_p' : 1,
            'frequency_penalty' : 0,
            'presence_penalty' : 0
        }
    }

    for section in parsed_product_spec:
        if section in label_to_prompt:
            prompt = label_to_prompt[section]

            prompt['prompt'] += f"\n\n{parsed_product_spec[section]}"

            prompts.append(prompt)
    return prompts

async def get_text(session, url, params):

    async with session.post(url, json = params) as resp:
        prompt_text = await resp.json()
        return prompt_text['choices'][0]['text']

async def main(url):

    prompts = get_prompts(parse_product_spec_text(extract_product_spec_text(extract_id_from_url(url))))
    
    async with aiohttp.ClientSession(headers = {'authorization' : 'Bearer sess-7G9MTV3wAzEtuVs3li8ZeUtLZXoooNFavnGhTbVO'}) as session:

        tasks = []
        for prompt in prompts:
            url = 'https://api.openai.com/v1/engines/text-davinci-002/completions'
            tasks.append(asyncio.ensure_future(get_text(session, url, prompt)))

        feedbacks = await asyncio.gather(*tasks)
        
    total_feedback = '\n\n'.join(feedbacks)

    feedback_summary = requests.post('https://api.openai.com/v1/engines/text-davinci-002/completions',
        headers = {'authorization' : 'Bearer sess-7G9MTV3wAzEtuVs3li8ZeUtLZXoooNFavnGhTbVO'},
        json = {
            'prompt' : f"The following text is written feedback of a product specification. Write a one-hundred fifty word summary of the feedback. The summary must be one paragraph and well-written.\n\nFEEDBACK\n\n{total_feedback}",
            'temperature' : 0.3,
            'max_tokens' : 512,
            'top_p' : 1,
            'frequency_penalty' : 0,
            'presence_penalty' : 0
        }
    ).json()
 
    return feedback_summary['choices'][0]['text']
    
summarization = asyncio.run(main('https://www.notion.so/IncSkill-Website-Product-Spec-673589270f7241dda9cb27fecab8af10'))
print(summarization)
#summarization = summarization.split("SPLITPOINT")