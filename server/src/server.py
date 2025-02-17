from datetime import datetime
import os
from agent import define_agent
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Tuple, Union
import numpy as np
from paco.execution_tree.execution_tree import ExecutionTree
from paco.execution_tree.execution_view_point import ExecutionViewPoint
from paco.explainer.build_explained_strategy import build_explained_strategy
from paco.explainer.strategy_view_point import StrategyViewPoint
from paco.parser.create import create
from paco.parser.tree_lib import CNode, CTree
from paco.saturate_execution.states import States
from paco.searcher.search import search
from utils.automa import calc_strategy_algo1, calc_strategy_algo2
from utils.env import ALGORITHMS, PATH_IMAGE_BPMN_LARK, PATH_IMAGE_BPMN_LARK_SVG, RESOLUTION, SESE_PARSER, sese_diagram_grammar
from utils.print_sese_diagram import print_sese_diagram
from paco.solver import paco
from utils.check_syntax import check_algo_is_usable, checkCorrectSyntax, check_input
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# TO EMBED DASH IN FASAPI
# https://medium.com/@gerardsho/embedding-dash-dashboards-in-fastapi-framework-in-less-than-3-mins-b1bec12eb3
# swaggerui al link  http://127.0.0.1:8000/docs
# server al link http://127.0.0.1:8000/
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)
class LoginRequest(BaseModel):
    username: str
    password: str
class BPMNDefinition(BaseModel):
    """
    Pydantic model for BPMN process definition
    
    Attributes:
        expression (str): BPMN process expression
        h (int, optional): Horizon value, defaults to 0
        probabilities (Dict, optional): Nature probabilities mapping
        impacts (Dict): Impact values for tasks
        loop_thresholds (Dict, optional): Thresholds for loops
        durations (Dict, optional): Task durations
        names (Dict, optional): Custom names mapping
        delays (Dict, optional): Delay values for choices
        impacts_names (List, optional): Names of impact metrics
        loop_round (Dict, optional): Loop round configurations
        loops_prob (Dict, optional): Loop probabilities
    """
    expression: str
    h: Optional[int] = 0
    probabilities: Optional[Dict] = {}
    impacts: Dict = {}
    loop_thresholds: Optional[Dict] = {}    
    durations: Optional[Dict] = {}
    names: Optional[Dict] = {}
    delays: Optional[Dict] = {}
    impacts_names: Optional[List] = []    
    loop_round: Optional[Dict] = {}
    loops_prob: Optional[Dict] = {}

class BPMNPrinting(BaseModel):
    """
    Model for BPMN diagram printing options
    
    Attributes:
        bpmn (BPMNDefinition): BPMN process definition
        resolution_bpmn (int, optional): Image resolution
        graph_options (Dict, optional): Graph rendering options
    """    
    bpmn: BPMNDefinition
    resolution_bpmn: Optional[int] = RESOLUTION
    graph_options: Optional[Dict] = {}

class StrategyFounderAlgo(BaseModel):
    """
    Model for strategy finding request
    
    Attributes:
        bpmn (BPMNDefinition): BPMN process definition
        bound (list[float]): Impact bounds vector
        algo (str): Algorithm selection
    """
    bpmn: BPMNDefinition
    bound: list[float]
    algo: str
# class ExecutionTreeModel(BaseModel):
#     """
#     Pydantic model representing an ExecutionTree structure
    
#     Attributes:
#         root: Root node of the execution tree
#         decisions: List of decision nodes
#         choices: List of choice nodes 
#         natures: List of nature nodes
#         transitions: Dictionary mapping transitions to next nodes
#         states: Current states of the tree
#     """
#     root: Union[ExecutionViewPoint, StrategyViewPoint]
#     decisions: List[CNode] = []
#     choices: List[CNode] = [] 
#     natures: List[CNode] = []
#     transitions: Dict[Tuple, 'ExecutionTree'] = {}
#     states: Optional[States] = None

#     def to_execution_tree(self) -> 'ExecutionTree':
#         """
#         Converts the model back to an ExecutionTree instance
#         """
#         tree = ExecutionTree(self.root)
#         tree.decisions = self.decisions
#         tree.choices = self.choices
#         tree.natures = self.natures
#         tree.transitions = self.transitions
#         tree.states = self.states
#         return tree
   
# class CNodeModel(BaseModel):
#     """
#     Pydantic model representing a CNode (Choice Node) structure
    
#     Attributes:
#         id (Optional[int]): Node identifier
#         name (Optional[str]): Node name
#         short_name (Optional[str]): Short version of node name
#         parent (Optional[CNodeModel]): Parent node
#         index_in_parent (int): Index position in parent's children
#         type (str): Node type ('task', 'sequential', 'parallel', 'natural', 'choice', 'loop', 'loop_probability')
#         impact (List): Impact values
#         non_cumulative_impact (List): Non-cumulative impact values
#         probability (Optional[float]): Probability for natural/choice nodes
#         ttr (int): Time to recovery
#         max_delay (float): Maximum delay allowed
#         duration (float): Duration of the task
#         incoming_impact_vectors (List): List of incoming impact vectors
#         is_leaf (bool): Whether the node is a leaf node
#         children (Optional[List[CTreeModel]]): Child nodes
#     """
#     id: Optional[int] = None
#     name: Optional[str] = None
#     short_name: Optional[str] = None
#     parent: Optional['CNodeModel'] = None
#     index_in_parent: int
#     type: str
#     impact: List = Field(default_factory=list)
#     non_cumulative_impact: List = Field(default_factory=list)
#     probability: Optional[float] = None
#     ttr: int = 0
#     max_delay: float = 0
#     duration: float = 0
#     incoming_impact_vectors: List = Field(default_factory=list)
#     is_leaf: bool = True
#     children: Optional[List['CTreeModel']] = None

#     class Config:
#         arbitrary_types_allowed = True

#     def to_cnode(self) -> 'CNode':
#         """
#         Converts the model back to a CNode instance
#         """
#         from paco.parser.tree_lib import CNode
#         node = CNode(
#             parent=self.parent.to_cnode() if self.parent else None,
#             index_in_parent=self.index_in_parent,
#             type=self.type,
#             id=self.id,
#             impact=self.impact,
#             non_cumulative_impact=self.non_cumulative_impact,
#             probability=self.probability,
#             name=self.name,
#             short_name=self.short_name,
#             ttr=self.ttr,
#             max_delay=self.max_delay,
#             duration=self.duration,
#             incoming_impact_vectors=self.incoming_impact_vectors
#         )
#         if self.children:
#             node.set_children([child.to_ctree() for child in self.children])
#         return node

#     @classmethod
#     def from_cnode(cls, node: 'CNode') -> 'CNodeModel':
#         """
#         Creates a CNodeModel instance from a CNode
        
#         Args:
#             node (CNode): The CNode instance to convert
            
#         Returns:
#             CNodeModel: The converted model
#         """
#         return cls(
#             id=node.id,
#             name=node.name,
#             short_name=node.short_name,
#             parent=cls.from_cnode(node.parent) if node.parent else None,
#             index_in_parent=node.index_in_parent,
#             type=node.type,
#             impact=node.impact,
#             non_cumulative_impact=node.non_cumulative_impact,
#             probability=node.probability,
#             ttr=node.ttr,
#             max_delay=node.max_delay,
#             duration=node.duration,
#             incoming_impact_vectors=node.incoming_impact_vectors,
#             is_leaf=node.isLeaf,
#             children=[CTreeModel.from_ctree(child) for child in node.children] if node.children else None
#         )
    
# class CTreeModel(BaseModel):
#     """
#     Pydantic model representing a CTree (Choice Tree) structure
    
#     Attributes:
#         root (CNodeModel): Root node of the choice tree
#     """
#     root: CNodeModel

#     class Config:
#         arbitrary_types_allowed = True

#     def to_ctree(self) -> 'CTree':
#         """
#         Converts the model back to a CTree instance
#         """
#         from paco.parser.tree_lib import CTree
#         return CTree(self.root.to_cnode())

#     @classmethod
#     def from_ctree(cls, tree: CTree) -> 'CTreeModel':
#         """
#         Creates a CTreeModel instance from a CTree
        
#         Args:
#             tree (CTree): The CTree instance to convert
            
#         Returns:
#             CTreeModel: The converted model
#         """
#         return cls(
#             root=CNodeModel.from_cnode(tree.root)
#         )
#######################################################
############ GET  #####################################
#######################################################
@app.get("/")
async def get():
    """
    Root endpoint that returns a welcome message
    Returns:
        str: Welcome message
    """
    return f"welcome to PACO server"


@app.get("/print_sese_diagram")
async def print_bpmn(request: BPMNPrinting, token: str = None) -> FileResponse:
    """
    Generates and returns a BPMN diagram image
    Args:
        request (BPMNPrinting): BPMN printing configuration
        token (str): Authorization token
    Returns:
        FileResponse: PNG image of the BPMN diagram
    Raises:
        HTTPException: 400 for invalid input, 500 for server errors, 403 for unauthorized access
    """
    bpmn = request.bpmn
    if token == None:
        raise HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(bpmn, BPMNDefinition):
        raise HTTPException(status_code=400, detail="Invalid input")
    if not checkCorrectSyntax(dict(bpmn)):
        raise HTTPException(status_code=400, detail="Invalid BPMN syntax")   
    try:
        
        try:
            img = print_sese_diagram(expression=bpmn.expression,
                h=bpmn.h, 
                probabilities=bpmn.probabilities, 
                impacts=bpmn.impacts, 
                loop_thresholds=bpmn.loop_thresholds, 
                outfile=f'src/{PATH_IMAGE_BPMN_LARK}', 
                outfile_svg=f'src/{PATH_IMAGE_BPMN_LARK_SVG}',
                graph_options=request.graph_options, 
                durations=bpmn.durations, 
                names=bpmn.names, 
                delays=bpmn.delays, 
                impacts_names=bpmn.impacts_names, 
                resolution_bpmn=request.resolution_bpmn, 
                loop_round=bpmn.loop_round, 
                loops_prob=bpmn.loops_prob
            )
            print('GRAPH' , img)
        except Exception as e:
            print('--------------------------------')
            print(e)
            print('--------------------------------')
            raise HTTPException(status_code=505, detail=str(e))
        return FileResponse(f'src/{PATH_IMAGE_BPMN_LARK}', media_type='image/png', filename='bpmn.png')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bpmn_img")
async def get_bpmn_img(name:str, token: str = None) -> FileResponse:
    """
    Returns the BPMN diagram image with the given name.
    Args:
        name (str): Name of the BPMN diagram image
        token (str): Authorization token
    Returns:
        FileResponse: PNG image of the BPMN diagram
    Raises:
        HTTPException: 403 for unauthorized access
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    return FileResponse(f'assets/bpmnSvg/{name}.png', media_type='image/png', filename=f'{name}.png')
@app.get("/bpmn_example_img")
async def get_bpmn_img(name:str, type:str = 'png', token: str = None) -> FileResponse:
    """
    Returns the BPMN diagram image with the given name.
    Args:
        name (str): Name of the BPMN diagram image
        token (str): Authorization token
    Returns:
        FileResponse: PNG image of the BPMN diagram
    Raises:
        HTTPException: 403 for unauthorized access
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    if type == 'svg':
        return FileResponse(f'assets/examples/{name}.svg', media_type='image/svg+xml', filename=f'{name}.svg')
    return FileResponse(f'assets/examples/{name}.png', media_type='image/png', filename=f'{name}.png')

@app.get("/check_correct_process_expression")
async def check_correct_process_expression(expression: str, token:str = None) -> bool:
    """
    Checks if the given BPMN process expression is correct according to the SESE diagram grammar.

    Args:
        expression (str): The BPMN process expression to be checked.

    Returns:
        bool: True if the expression is correct and can be parsed by SESE_PARSER, False otherwise.

    Raises:
        Exception: If the expression cannot be parsed, an exception is caught and False is returned.
        403: If the token is not provided, an exception not authorized.
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    try:
        SESE_PARSER.parse(expression)
        return True
    except Exception as e:
        return False

@app.get("/bpmn_grammar")
async def get_grammar(
    token:str = None
    ) -> str:
    """
    Returns the SESE diagram grammar.

    Returns:
        str: The SESE diagram grammar.

    Raises:
        403: If the token is not provided, an exception not authorized.
    """
    if token == None:
        raise HTTPException(status_code=403, detail="Not authorized")
    try:
        return sese_diagram_grammar
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/check_input")
async def check_input_bpmn(bpmn: BPMNDefinition, bound: list[float], token:str = None) -> tuple[str, List[int]]:
    """
    Checks the input of the given BPMN process and bound.

    Args:
        bpmn (BPMNDefinition): The BPMN process to be checked.
        bound (list[float]): The bound to be checked.

    Returns:
        str: An error message if the input is not valid, an empty string otherwise.

    Raises:
        400: If the input is not valid, an exception is raised.
        403: If the token is not provided, an exception not authorized.
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(bpmn, BPMNDefinition) or not isinstance(bound, list):
        return HTTPException(status_code=400, detail="Invalid input")
    try:

        check_input(dict(bpmn), bound)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.get("/check_algo_usable")
async def check_algo_usable(sfa :StrategyFounderAlgo, token:str = None) -> bool:
    """
    Checks if the given algorithm is usable for the given BPMN process.

    Args:
        bpmn (BPMNDefinition): The BPMN process to be checked.
        algo (str): The algorithm to be checked.

    Returns:
        bool: True if the algorithm is usable, False otherwise.

    Raises:
        400: If the algorithm is not valid, an exception is raised.
        403: If the token is not provided, an exception not authorized.
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(sfa.bpmn, BPMNDefinition) or not isinstance(sfa.algo, str):
        return HTTPException(status_code=400, detail="Invalid input")
    if not check_algo_is_usable(sfa.bpmn.expression, sfa.algo):
        return False
    return True

@app.get("/check_syntax")
async def check_syntax(bpmn: BPMNDefinition, token:str = None) -> bool:
    """
    Checks the syntax of the given BPMN process.

    Args:
        bpmn (BPMNDefinition): The BPMN process to be checked.

    Returns:
        bool: True if the syntax is correct, False otherwise.

    Raises:
        400: If the input is not valid, an exception is raised.
        403: If the token is not provided, an exception not authorized.
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(bpmn, BPMNDefinition):
        return HTTPException(status_code=400, detail="Invalid input")
    return checkCorrectSyntax(dict(bpmn))

@app.get("/get_algorithms") 
async def get_algorithms(token:str = None) -> List[str]:
    """
    Returns the list of available algorithms.

    Returns:
        List[str]: The list of available algorithms.

    Raises:
        403: If the token is not provided, an exception not authorized.
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    try:
        return list(ALGORITHMS.values())
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.get("/calc_strategy_general")
async def calc_strategy_and_explainer(request: StrategyFounderAlgo, token: str = None) -> dict:
    """
    Calculates strategy using PACO algorithm
    Args:
        request (StrategyFounderAlgo): Strategy calculation parameters
    Returns:
        dict: Calculation results
    Raises:
        HTTPException: 400 for invalid input, 500 for server errors
    """
    if token == None:
        raise HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(request.bpmn, BPMNDefinition):
        raise HTTPException(status_code=400, detail="Invalid input")
    bpmn = dict(request.bpmn)
    if not checkCorrectSyntax(bpmn):
        raise HTTPException(status_code=400, detail="Invalid BPMN syntax")
    if not check_algo_is_usable(bpmn, request.algo):
        raise HTTPException(status_code=400, detail="The algorithm is not usable")       
    try:
        bound = np.array(request.bound, dtype=np.float64)            
        if request.algo == list(ALGORITHMS.keys())[0]:
            text_result, parse_tree, execution_tree, found, min_expected_impacts, max_expected_impacts, choices, name_svg = paco(bpmn, bound)
        elif request.algo == list(ALGORITHMS.keys())[1]:
            text_result, found, choices, name_svg = calc_strategy_algo1(bpmn, bound)
        elif request.algo == list(ALGORITHMS.keys())[2]:
            text_result, found, choices, name_svg = calc_strategy_algo2(bpmn, bound)
        else:
            return HTTPException(status_code=400, detail="Invalid algorithm")

        return {
            "text_result": text_result,
            "parse_tree": parse_tree,
            "execution_tree": execution_tree,
            "found": found,
            "min_expected_impacts": min_expected_impacts.tolist() if min_expected_impacts is not None else None,
            "max_expected_impacts": max_expected_impacts.tolist() if max_expected_impacts is not None else None,
            "choices": choices,
            "name_svg": name_svg
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/excecution_tree")
async def get_excecution_tree(bpmn:BPMNDefinition = None, token:str = None) -> tuple: #[CTreeModel, ExecutionTreeModel]:
    """
    Get the execution tree.

    Args:
        token (str): The token of the agent.
        bpmn (BPMNDefinition): The BPMN process.

    Returns:
        tuple: The parse tree & execution tree.

    Raises:
        403: If the token is not provided, an exception not authorized.
        400: If the input is not valid, an exception is raised.
        500: If an error occurs, an exception is raised.
    """
    if token == None:
        raise HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(bpmn, BPMNDefinition) or bpmn == None:
        raise HTTPException(status_code=400, detail="Invalid input")
    try:        
        parse_tree, execution_tree = create(dict(bpmn))
        return {
            "parse_tree": parse_tree,
            "execution_tree": execution_tree
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/search_only_strategy")
async def search_strategy(
    impacts_names: list[str], execution_tree, #: ExecutionTreeModel, 
    bound: list[float], search_only: bool, token:str = None
    ) -> tuple:
    """
    calcolate ONLY the strategy.
    Args:
        impacts_names (list[str]): The impacts names.
        execution_tree (ExecutionTreeModel): The execution tree.
        bound (np.ndarray): The bound.
        search_only (bool): If True, only search for a solution without building the strategy.
        token (str): The token of the agent.

    Returns:
        tuple: The expected impacts, possible min solution, solutions, and strategy.

    Raises:
        403: If the token is not provided, an exception not authorized.
        400: If the input is not valid, an exception is raised.
        500: If an error occurs, an exception is raised.
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(impacts_names, list[str]) or not isinstance(bound, np.ndarray) or not isinstance(search_only, bool):
        return HTTPException(status_code=400, detail="Invalid input")
    try:

        expected_impacts, possible_min_solution, solutions, strategy = search(
            execution_tree#.to_execution_tree()
            , bound, impacts_names, search_only
        )

        if expected_impacts is None:
            text_result = ""
            for i in range(len(possible_min_solution)):
                text_result += f"Exp. Impacts {i}:\t{np.round(possible_min_solution[i], 2)}\n"
            #print(f"Failed:\t\t\t{bpmn.impacts_names}\nPossible Bound Impacts:\t{bound}\n" + text_result)
            text_result = ""
            for i in range(len(solutions)):
                text_result += f"Guaranteed Bound {i}:\t{np.ceil(solutions[i])}\n"

            #print(str(datetime.now()) + " " + text_result)
            return {
                "text_result": text_result,
                "expected_impacts": expected_impacts,
                "possible_min_solution": possible_min_solution,
                "solutions": solutions,
                "strategy": []
            }

        if strategy is None:
            text_result = f"Any choice taken will provide a winning strategy with an expected impact of: "
            text_result += " ".join(f"{key}: {round(value,2)}" for key, value in zip(impacts_names,  [item for item in expected_impacts]))
            print(str(datetime.now()) + " " + text_result)
            return {
                "text_result": text_result,
                "expected_impacts": expected_impacts,
                "possible_min_solution": possible_min_solution,
                "solutions": solutions,
                "strategy": []
            }
        text_result = f"This is the strategy, with an expected impact of: "
        text_result += " ".join(f"{key}: {round(value,2)}" for key, value in zip(impacts_names,  [item for item in expected_impacts]))

        return {
            "text_result": text_result,
            "expected_impacts": expected_impacts,
            "possible_min_solution": possible_min_solution,
            "solutions": solutions,
            "strategy": strategy
        }

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.get("/explainer")
async def get_explainer(
    parse_tree#: CTreeModel
    , strategy, type_strategy: str, impacts_names: list[str], name_svg: str = '', token:str = None
    ) -> tuple:
    """
    Get the explainer.

    Args:
        parse_tree (CTree): The parse tree.
        strategy: The strategy.
        type_strategy (str): The type of strategy.
        impacts_names (list[str]): The impacts names.
        name_svg (str): The name of the svg.
        token (str): The token of the agent.

    Returns:
        tuple: The strategy tree, expected impacts, strategy expected time, choices, and name svg.

    Raises:
        403: If the token is not provided, an exception not authorized.
        400: If the input is not valid, an exception is raised.
        500: If an error occurs, an exception is raised.
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(strategy, list) or not isinstance(type_strategy, str) or not isinstance(impacts_names, list[str]) or not isinstance(name_svg, str):
        return HTTPException(status_code=400, detail="Invalid input")
    try:
        strategy_tree, expected_impacts, strategy_expected_time, choices, _ = build_explained_strategy(
            parse_tree #.to_ctree()
            , strategy, type_strategy, impacts_names, name_svg
        )
        return  {
            "strategy_tree": strategy_tree,
            "expected_impacts": expected_impacts,
            "strategy_expected_time": strategy_expected_time,
            "choices": choices,
            "name_svg": name_svg
        }
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

#######################################################
###             LLMS API                            ###
#######################################################
@app.get("/agent-definition")
async def get_agent(
    url: str, api_key: str, 
    model: str, temperature: float,
    token: str = None,
    ):
    """
    Define the agent with the given parameters.

    Args:
        url (str): The url of the agent.
        api_key (str): The api key of the agent.
        model (str): The model of the agent.
        temperature (float): The temperature of the agent.
        token (str): The token of the agent.

    Returns:
       tuple: The agent defined and the configuration.
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(url, str) or not isinstance(api_key, str) or not isinstance(model, str) or not isinstance(temperature, float):
        return HTTPException(status_code=400, detail="Invalid input")
    try:
        llm, config =  define_agent(url, api_key, model, temperature)
        return {
            "llm": llm,
            "config": config
        }
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.get("/invoke-agent")
async def invoke_agent(prompt:str, llm, history:list[tuple],  token:str = None) ->  tuple[str, list[tuple]]:
    """
    Invoke the agent with the given prompt.

    Args:
        prompt (str): The prompt to be used.
        token (str): The token of the agent.
        llm: The agent defined.
        history: The history of the agent.

    Returns:
        str: The response from the agent.
        list[tuple]: The history of the agent.
    """
    if token == None:
        return HTTPException(status_code=403, detail="Not authorized")
    if not isinstance(prompt, str):
        return HTTPException(status_code=400, detail="Invalid input")
    try:
        response = llm.invoke({"input": prompt})
        history.append((prompt, response.content))
        return {
            "response": response.content,
            "history": history
        }
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


#######################################################
############ POST #####################################
#######################################################

@app.post("/login")
async def login(request: LoginRequest):
    """
    Login endpoint
    
    Args:
        request (LoginRequest): Login credentials
            username (str): Username
            password (str): Password
    
    Returns:
        dict: Login response containing token
        
    Raises:
        HTTPException: 401 for invalid credentials
    """
    if request.username == 'admin' and request.password == 'admin':
        return {"token": os.urandom(24).hex()}
    raise HTTPException(status_code=401, detail="Invalid credentials")


#######################################################
############ PUT ######################################
#######################################################

# @app.put("/update")
# async def put():
#     pass

#######################################################
############ DELETE ###################################
#######################################################

# @app.delete("/delete")
# async def delete():
#     pass

#######################################################
#### MAIN #############################################
#######################################################

if __name__ == '__main__':   
    uvicorn.run(
        app, 
        host="0.0.0.0", port=8000,
        # ssl_keyfile=os.getenv("SSL_KEY"),      # Optional: SSL key
        # ssl_certfile=os.getenv("SSL_CERT")   # Optional: SSL certificate
    )
