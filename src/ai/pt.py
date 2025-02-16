# # Example: reuse your existing OpenAI setup
from openai import OpenAI
# from prompt import examples_prompt
# # Point to the local server
client = OpenAI(base_url="http://157.27.193.108:1234/v1", api_key="lm-studio")
prompt = "Always answer in rhymes. Talk about the future, and the past, and the present times."
sms = [ {'role' : 'system', 'content' : 'You are an assistant to design processes. In particular, your role is to pass from an user description of the process to the grammar defined using the python library lark and vice versa.  '} ]
m = "lmstudio-community/Llama-3.1-Nemotron-70B-Instruct-HF-GGUF"
# for p in list(examples_prompt.keys()):
#     print(examples_prompt[p])
#     sms.append({"role": "user", "content": examples_prompt[p]})
completion = client.chat.completions.create(
  model=m,
  messages=sms,
  temperature=0.7,
)

print(completion.choices[0].message.content)

# while True:
#   completion = client.chat.completions.create(
#       model = m,
#       messages = sms,
#       temperature = 0.7,
#       stream=True
#   )
  
#   prompt = {'role': 'system' , 'content':''} 
#   for chunk in completion:
#     if chunk.choices[0].delta.content:
#       print(chunk.choices[0].delta.content, end="", flush=True)
#       prompt['content'] = chunk.choices[0].delta.content
#   sms.append(prompt)
#   print('---------------------------------------------------------------------------------------------------')
#   print('---------------------------------------------------------------------------------------------------')
#   print('---------------------------------------------------------------------------------------------------')
#   print('---------------------------------------------------------------------------------------------------')
#   sms.append({'role': 'user' , 'content':input("insert prompt : ")})
# from langchain.memory import ConversationBufferMemory
# from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains import LLMChain
from langchain.llms import OpenAI  # Assuming you're using OpenAI's model, replace with LM Studio LLM import if different
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
# template = """You are an AI chatbot having a conversation with a human.

# {history}
# Human: {human_input}
# AI: """

# prompt = PromptTemplate(template=prompt) #(input_variables=["history", "human_input"], template=template)
# # msgs = StreamlitChatMessageHistory(key="special_app_key")
# # memory = ConversationBufferMemory(memory_key="history", chat_memory=msgs)
# # if len(msgs.messages) == 0:
# #     msgs.add_ai_message("How can I help you?")
# llm_chain = LLMChain(llm=client, prompt=prompt)
# response = llm_chain.run(prompt)
# print(response)

llm: ChatOpenAI = ChatOpenAI(
    base_url="http://157.27.193.108:1234/v1",
    temperature=0.7,
    api_key="lm-studio",
    model = m
)
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    print("Using tool")
    return len(word)


tools = [get_word_length]
llm_with_tools = llm.bind_tools(tools=tools)
print(llm_with_tools)
print('----------------')
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but don't know current events",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
list(agent_executor.stream(
    {"input": "what is the length of characters in the word eudca"}))

print('----------------')
list(agent_executor.stream(
    {"input": input("insert prompt : ")}))
print('finito')