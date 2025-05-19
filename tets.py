import openai
openai.api_key = ''

messages = [{'role': 'system', 'content': 'You are a helpful chat assistant'}]

while True:
    message = input('User: ')
    if message:
        messages.append({'role': 'user', 'content': message})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
        reply = response['choices'][0]['message']['content']
        print(f'Assistant: {reply}')
        messages.append({'role': 'assistant', 'content': reply})
       
