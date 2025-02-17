import base64
import os
import aiohttp
import requests

from env import URL_SERVER
headers = {
    "Content-Type": "application/json",
}
#################################
# API FILE
#################################


########################
# LLM - AI
########################
async def get_agent_definition(token = None):
    agent_definition = requests.get(
        f'{URL_SERVER}agent-definition',
        params={'token': token},
        headers=headers,
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
        params={'token': token},
        headers=headers,
    )
    if ag.status_code == 200:
        return ag.json()['response'], ag.json()['history']
    return None

########################
# AUTHORIZATION FUNCTION
########################
async def authorization_function(username = '', password = '', server = None):
    """
    Authenticate user and store token
    Returns: Tuple[bool, Optional[str]] - (is_authorized, token)
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{URL_SERVER}login",
                json={"username": username, "password": password},
                headers=headers,
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    token = data.get('token')
                    if token:
                        return True, token, server.config.update(
                                                SECRET_KEY=os.environ.get('SECRET_KEY', os.urandom(24).hex()),
                                                SESSION_TYPE='filesystem',
                                                SESSION_FILE_DIR='flask_session'
                                            )
        return False, None
    except Exception as e:
        print(f"Auth error: {e}")
        return False, None
    


########################
# BPMN 
########################


def get_image_content(name: str, type: str = 'png', token: str = None) -> str:
    """
    Get image content from the API synchronously
    
    Args:
        name (str): Name of the image
        type (str): Image type ('png' or 'svg')
        token (Optional[str]): Authentication token
        
    Returns:
        Optional[str]: Base64 encoded image content or None if failed
    """
    try:
        print('url', f'{URL_SERVER}bpmn_example_img')
        response = requests.get(
            f'{URL_SERVER}bpmn_example_img',
            params={'name': name, 'type': type, 'token': token},
            headers=headers,
        )
        if response.status_code == 200:
            return base64.b64encode(response.content).decode()
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")
        return None


def get_bpmn_grammar(token = None):
    bpmn_grammar = requests.get(
        f'{URL_SERVER}bpmn_grammar',
        params={'token': token},
        headers=headers,
    )
    if bpmn_grammar.status_code == 200:
        return bpmn_grammar.json()['grammar']
    return None