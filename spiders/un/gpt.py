import g4f
import os

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

print(g4f.Provider.Ails.params) # supported args

# Automatic selection of provider

# streamed completion
# response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', messages=[
#                                      {"role": "user", "content": "Hello world"}], stream=True)

# for message in response:
#     print(message)

# # normal response
response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, messages=[
                                     {"role": "user", "content": "hi"}]) # alterative model setting

print(response)


# # Set with provider
# response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.Forefront, messages=[
#                                      {"role": "user", "content": "Hello world"}], stream=True)

# for message in response:
#     print(message)