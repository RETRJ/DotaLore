import os
import openai
import tiktoken
import itemDescGetter
import random
import DialogExporter
import time

openai.api_key = "bruh"


def num_tokens_from_string(string: str, encoding_name="gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def getSysInfo(items, limit: int, bigData=False):
    ALL = set()
    print(items)
    if bigData:
        for i in items:
            ALL.update(itemDescGetter.getTopicsFor(i))
    else:
        for i in items:
            ALL.update([i])

    print(ALL)
    print(len(ALL))
    sysinf = ""
    percentage = 100

    tokens = 999999999
    while tokens >= limit and percentage >= 0:
        sysinf = ""
        for i in ALL:
            if i in items or random.randint(1, 100) <= percentage:
                tmp = itemDescGetter.getStr(i, i in items)
                if tmp:
                    sysinf += f"[{tmp}]\n"

        tokens = num_tokens_from_string(sysinf)
        print(f"tokens: {tokens} at {percentage}%")
        percentage -= tokens / limit * 2

    return sysinf


# dialog1 = '''According to data given: How "Dark Willow" and "Bounty Hunter" are related, even indirectly? Do not make things up, answer in maximum 3 sentences.
# '''
#
# ans = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=[
#    {"role": "system", "content": f"{system_info}"},
#    {"role": "user", "content": f"{dialog1}"}],
#                                   temperature=0.3,
#                                   top_p=1,
#                                   max_tokens=200,
#                                   presence_penalty=0,
#                                   frequency_penalty=0,
#                                   n=1)

def createDialogBetween(*items: str, n=1):
    chars = []
    for i in items:
        chars.append(i)
    if len(chars) < 2:
        chars.append("Human")

    for i in range(n):
        system_info = getSysInfo(chars, 1)
        pre_instruction = f'''According to data given: What are the relationships and attitude towards each other between "{chars[0]}" and "{chars[1]}", even indirect ones? Don't mention Dota 2.
        '''

        ans = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=[
            {"role": "system", "content": system_info},
            {"role": "user", "content": pre_instruction}],
                                           temperature=0.2,
                                           top_p=1,
                                           max_tokens=500,
                                           presence_penalty=0,
                                           frequency_penalty=0,
                                           n=1)

        instruction = f'''According to data given: Create a long dialog between "{chars[0]}" and "{chars[1]}", consider that: \n{ans['choices'][0]['message']['content']}\n
        '''

        print(f'Dialog #{i + 1}: {instruction}')

        system_info = getSysInfo(chars, 11000, True)
        ans = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=[
            {"role": "system", "content": system_info},
            {"role": "user", "content": instruction}],
                                           temperature=1.1,
                                           top_p=0.95,
                                           max_tokens=3000,
                                           presence_penalty=0.3,
                                           frequency_penalty=0.75,
                                           n=1)
        for res in ans['choices']:
            DialogExporter.saveDialog(res['message']['content'], chars)
        time.sleep(50)


createDialogBetween("Bristleback","Tusk" , n=2)
