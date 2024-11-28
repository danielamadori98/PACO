from utils.env import sese_diagram_grammar
define_role = f'''

    You are an assistant to design processes. In particular, 
    your role is to pass from an user description of the process to the grammar defined using the python library lark and vice versa.  
    Note that all process that you have to create are BPMN diagram that are single-entry-single-exit (SESE). 
    Meaning that for all nodes you have only one element in exit and one incoming.        
    There are few exceptions which are: natures or probabilistic split, choice and parallel. They have one entry but 2 exits.
    That is because the the choices and the natures represents xor decisions while parallel represents 'and', so taking both the branches.
    the grammar is {sese_diagram_grammar}.
    All the different section of the process are inserted in () and there can not be an empty region. These can be nested as (T1, (T2,T3)).
    '''

examples_bpmn = [
    {
        "input": '''
        depicts a metal manufacturing process that involves cutting, milling,
        bending, polishing, depositioning, and painting a metal piece. 
        First the cutting is done. Then, I have to do both:
        - bending and then there is a nature that decides between heavy or light polishing
        - milling, then I have a choice between fine or rough deposition
        after this there is a choice between the hphs or lpls painting.
        With this choice the process is concluded. 
        ''',
        "answer": '''
        (Cutting, ( (Bending, (HP ^ [N1]LP ) ) || ( Milling, ( FD / [C1] RD))), (HPHS / [C2] LPLS))
        ''',

    },

    {
        "input": ''' I have a process where at the beginnig the user has to do 5 surveys (call them S1, S2,S3, ...) alltogheter. 
        Then, Based on the answer there is a nature that send me or in a T1 or T2. After I have 2 choises to make.
        ''',
        "answer": '''(S1 || S2 || S3 || S4 || S5), (T1 ^ [N1] T2), (C1 / [C2] C2)''',

    },

    {
        "input": '''I have a process where I do a simpletask1 before a task1''',
        "answer": '''(SimpleTask1, Task1)''',

    },

    # {
    #     "input": '''Now I have to complete the writing task before having a nature between talking with the publisher or to print the page written. Then, i choose between going to the park or continue writing''',
    #     "answer": '''(Writing, (Talking with Publisher ^ [N1] Print Page), (Go to the Park / [C1] Continue Writing))''',

    # },

    # {
    #     "input": '''''',
    #     "answer": '''''',

    # },
]



a = {
    'prompt' : '''

    You are an assistant to design processes. In particular, 
    your role is to pass from an user description of the process to the grammar defined using the python library lark and vice versa.  
    Note that all process that you have to create are BPMN diagram that are single-entry-single-exit (SESE). 
    Meaning that for all nodes you have only one element in exit and one incoming.        
    There are few exceptions which are: natures or probabilistic split, choice and parallel. They have one entry but 2 exits.
    That is because the the choices and the natures represents xor decisions while parallel represents 'and', so taking both the branches.
    the grammar is """
    ?start: xor

    ?xor: parallel
        | xor "/" "[" NAME "]" parallel -> choice
        | xor "^" "[" NAME "]" parallel -> natural

    ?parallel: sequential
        | parallel "||" sequential  -> parallel

    ?sequential: region
        | sequential "," region -> sequential    

    ?region: 
        | NAME   -> task
        | "<" xor ">" -> loop
        | "<" "[" NAME "]"  xor ">" -> loop_probability
        | "(" xor ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
    """.
    All the different section of the process are inserted in () and there can not be an empty region. These can be nested as (T1, (T2,T3)).
    Here an example. 
    User: 
    depicts a metal manufacturing process that involves cutting, milling,
    bending, polishing, depositioning, and painting a metal piece. 
    First the cutting is done. Then, I have to do both:
    - bending and then there is a nature that decides between heavy or light polishing
    - milling, then I have a choice between fine or rough deposition
    after this there is a choice between the hphs or lpls painting.
    With this choice the process is concluded. 

    The traduction is: (Cutting, ( (Bending, (HP ^ [N1]LP ) ) || ( Milling, ( FD / [C1] RD))), (HPHS / [C2] LPLS))
    
    Another example: 
    I have a process where at the beginnig the user has to do 5 surveys (call them S1, S2,S3, ...) alltogheter. 
    Then, Based on the answer there is a nature that send me or in a T1 or T2. After I have 2 choises to make.
    
    the traduction: (S1 || S2 || S3 || S4 || S5), (T1 ^ [N1] T2), (C1 / [C2] C2)
    
    Another example:
    I have a process where I do a simpletask1 before a task1
    The traduction: (SimpleTask1, Task1)

    Another example:
    Now I have to complete the writing task before having a nature between talking with the publisher or to print the page written. Then, i choose between going to the park or continue writing
    the traduction: (Writing, (Talking with Publisher ^ [N1] Print Page), (Go to the Park / [C1] Continue Writing))
    ''', 

    'prompt1' : '''
    All the different section of the process are inserted in (). These can be nested as (T1, (T2,T3)). 
    Moreover there can not be an empty region.
    Now write your answer in sections. In particular, the first section has to have the summary with the translation of the process given and a second one where you provide the total answer. Now translate this process: i have a machine that melts a piece of iron. Then, the melted iron is divided into 2 different baskets. The first is cast into a nail shape and has to be individually checked. There is a probability that some are not correct; in this case, they are collected in a special bucket. if they are correct are packed and then shipped. The other iron is cast into cubes and are decided that are shipped to the customer or put into the warehouse. then if the shipped is made the accountant  send the bills.
    ''', 
}

examples = [
    {
        "question": '''''',
        "answer": '''''',

    },
    {
        "question": "When was the founder of craigslist born?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952
""",
    },
    {
        "question": "Who was the maternal grandfather of George Washington?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the mother of George Washington?
Intermediate answer: The mother of George Washington was Mary Ball Washington.
Follow up: Who was the father of Mary Ball Washington?
Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
So the final answer is: Joseph Ball
""",
    },
    {
        "question": "Are both the directors of Jaws and Casino Royale from the same country?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who is the director of Jaws?
Intermediate Answer: The director of Jaws is Steven Spielberg.
Follow up: Where is Steven Spielberg from?
Intermediate Answer: The United States.
Follow up: Who is the director of Casino Royale?
Intermediate Answer: The director of Casino Royale is Martin Campbell.
Follow up: Where is Martin Campbell from?
Intermediate Answer: New Zealand.
So the final answer is: No
""",
    },
]