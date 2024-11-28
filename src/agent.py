import random
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.agents import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from prompt import examples_bpmn, define_role
memory = MemorySaver()
model: ChatOpenAI = ChatOpenAI(
    base_url="http://157.27.193.108:1234/v1",
    temperature=0.7,
    api_key="lm-studio",
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
print(few_shot_prompt.invoke({}).to_messages())
chain = final_prompt | model

chain.invoke({"input": "I have to complete the writing task before having a nature between talking with the publisher or to print the page written. Then, i choose between going to the park or continue writing"})
# @tool
# def get_word_length(word: str) -> int:
#     """Returns the length of a word."""
#     print("Using tool")
#     return random.randint(0, 10)

# tools = [get_word_length]
# agent_executor = create_react_agent(model, tools, checkpointer=memory)

# # Use the agent
# config = {"configurable": {"thread_id": "abc123"}}
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