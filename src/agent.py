from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from ai.prompt import examples_bpmn, define_role
from utils.env import MODEL, SESE_PARSER
# https://github.com/RenaudLN/dash_socketio/tree/main

# docker build -t paco .
# docker run -d -p 8050:8050 -it --name paco paco 

@tool
def check_correct_process(expression: str) -> bool:
    """
    Checks if the given BPMN process expression is correct according to the SESE diagram grammar.

    Args:
        expression (str): The BPMN process expression to be checked.

    Returns:
        bool: True if the expression is correct and can be parsed by SESE_PARSER, False otherwise.

    Raises:
        Exception: If the expression cannot be parsed, an exception is caught and False is returned.
    """
    try:
        SESE_PARSER.parse(expression)
        return True
    except Exception as e:
        return False



# url = '157.27.193.108'
# memory = MemorySaver()
# model: ChatOpenAI = ChatOpenAI(
#     base_url=f"http://{url}:1234/v1",
#     temperature=0.7,
#     api_key="lm-studio",
# )

# example_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("human", "{input}"),
#         ("ai", "{answer}"),
#     ]
# )

# few_shot_prompt = FewShotChatMessagePromptTemplate(
#     example_prompt=example_prompt,
#     examples=examples_bpmn,
# )

# final_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", define_role),
#         few_shot_prompt,
#         ("human", "{input}"),
#     ]
# )
# print(few_shot_prompt.invoke({}).to_messages())
# chain = final_prompt | model
# config = {"configurable": {"thread_id": "abc123"}}
# chain.invoke(
#     {"input": "I have to complete the writing task before having a nature between talking with the publisher or to print the page written. Then, i choose between going to the park or continue writing"})
# for chunk in chain.stream(
    
#     {"input": [HumanMessage(content="I have to complete the writing task before having a nature between talking with the publisher or to print the page written. Then, i choose between going to the park or continue writing")]}, config
# ):
#     print(chunk.content, end='', flush=True)
# while True:
#     user_input = input("You: ")
#     for chunk in chain.stream(
#         {"input": user_input}, config
#     ):
#         print(chunk.content, end='', flush=True)

def define_agent(
        url = '157.27.193.108', verbose = False,
        api_key = "lm-studio",
        model = MODEL,
        temperature = 0.7
    ):  
    """
    Define the agent to be used in the chatbot.
    
    Args:
        url (str): The url of the agent.
        verbose (bool): Whether to print the output of the agent.
        api_key (str): The api key of the agent.
        model (str): The model of the agent.
        temperature (float): The temperature of the agent.
        
    Returns:
        tuple: The agent defined and the configuration.
    """
    if url.startswith("http"):
        base_url = url
    else: 
        base_url = f"http://{url}:1234/v1" 
    model: ChatOpenAI = ChatOpenAI(
        base_url=base_url,
        temperature=temperature,
        api_key=api_key,
        model=MODEL
    )

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{answer}"),
        ]
    )

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples_bpmn,
    )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", define_role),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )
    if verbose:
        print(few_shot_prompt.invoke({}).to_messages())
    chain = final_prompt | model
    config = {"configurable": {"thread_id": "abc123"}}
    if verbose:
        try:
            chain.invoke(    {"input": "I have to complete the writing task before having a nature between talking with the publisher or to print the page written. Then, i choose between going to the park or continue writing"})
        except Exception as e:
            print(e)
    return chain, config

# chain, config = define_agent(verbose=True)
# chain.invoke(
#     {"input": "I have to complete the writing task before having a nature between talking with the publisher or to print the page written. Then, i choose between going to the park or continue writing"})

# tools = [get_word_length]
# agent_executor = create_react_agent(model, tools, checkpointer=memory)

# # Use the agent

# for chunk in agent_executor.stream(
#     {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config
# ):
#     print(chunk)
#     print("----")

# for chunk in agent_executor.stream(
#     {"messages": [HumanMessage(content="whats the weather where I live?")]}, config
# ):
#     print(chunk)
#     print("----")