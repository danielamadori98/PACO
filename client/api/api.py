import base64
import requests

from env import URL_SERVER

#################################
# API FILE
#################################


########################
# LLM - AI
########################
async def get_agent_definition(token = None):
    agent_definition = requests.get(
        f'{URL_SERVER}agent-definition',
        params={'token': token}
    )
    if agent_definition.status_code == 200:
        llm = agent_definition.json()['llm']
        config = agent_definition.json()['config']
        return llm, config
    return None

async def invoke_llm(llm, prompt, token= None):
    ag = requests.post(
        f'{URL_SERVER}invoke',
        json={'llm': llm, 'prompt': prompt},
        params={'token': token}
    )
    if ag.status_code == 200:
        return ag.json()['response'], ag.json()['history']
    return None

########################
# AUTHORIZATION FUNCTION
########################
async def authorization_function(username = '', password = ''):
    """
    Authenticate user and store token
    Returns: Tuple[bool, Optional[str]] - (is_authorized, token)
    """
    try:
        resp = requests.get(
            f"{URL_SERVER}login", 
            json={"username": username, "password": password}
        )
        if resp.status_code == 200:
            token = resp.json().get('token')
            if token:
                return True, token
        return False, None
    except Exception as e:
        print(f"Auth error: {e}")
        return False, None
    


########################
# BPMN 
########################


async def get_image_content(name, type='png', token=None) -> str:
    """Get image content from the API"""
    response = requests.get(
        f'{URL_SERVER}bpmn_example_img',
        params={'name': name, 'type': type, 'token': token}
    )
    if response.status_code == 200:
        return base64.b64encode(response.content).decode()
    return None

async def get_bpmn_grammar(token = None):
    bpmn_grammar = requests.get(
        f'{URL_SERVER}bpmn_grammar',
        params={'token': token}
    )
    if bpmn_grammar.status_code == 200:
        return bpmn_grammar.json()
    return None