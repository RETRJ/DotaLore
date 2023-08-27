import os
import openai


openai.api_key = "code"

system_info = '''[WORLD DATA HERE]
'''

dialog_type = '''INSTRUCT HERE
'''
dialog = '''Write a long dialog beetwen [HERO1] and [HERO2]. [HERO1] is an awful and rude. Write only dialog.
'''
ans = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=[
    {"role":"system", "content": f"{system_info}"},
    {"role": "user", "content": f"{dialog}"}],
                                   temperature= 1.2,
                                   top_p= 0.95,
                                   max_tokens=4000,
                                   presence_penalty= 0.5,
                                   frequency_penalty= 0.5,
                                   n=1)
k=1
for res in ans['choices']:
    print(f"\n\n########## DIALOG №{k} ############\n\n")
    k+=1
    print(res['message']['content'])