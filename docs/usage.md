---
title: Usage Guide
layout: default
---

# Usage Guide

## Syntax and Basic Components

In the following section, you can check the syntax of a BPMN file and the basic components of the language togheter with useful examples. The BPMN language is transformed in a lark grammar and the syntax is checked using the lark parser. Here is the complete grammar:
?start: xor

?xor: parallel | xor "/" "" NAME "" parallel -> choice | xor "^" "" NAME "" parallel -> natural

?parallel: sequential | parallel "||" sequential -> parallel

?sequential: region | sequential "," region -> sequential

?region: | NAME -> task | "<" xor ">" -> loop | "<" "" NAME "" xor ">" -> loop_probability | "(" xor ")"

%import common.CNAME -> NAME %import common.NUMBER %import common.WS_INLINE

%ignore WS_INLINE

---

### Tasks

The tasks are the most basic element of a BPMN diagram. They represent the work that needs to be done. Tasks are defined using the following syntax: To define a simple task it is sufficient to digit the name. The task can be done by a person or an adversary. To define the task made by the person, just write the name of the task. To define the task made by the adversary, just write the name of the task and put a "_" at the beginning. Example: 'Do something' -> simple task made by the person '_Do something' -> simple task made by the adversary

**Example:**
- `"Do something"` -> simple task performed by the person
- `"_Do something"` -> task performed by the adversary

#### Task example of a person

![Task example of a person](../src/assets/examples/simple_person_task.png)

#### Task example of an adversary

![Task example of an adversary](../src/assets/examples/_SimpleAdversaryTask.png)

Each task has also a duration and an impact factor. Both are mandatory. Duration is an interval that can be between 0 and infinite. If they are not specified, the default values are 0 and infinitive. Otherwise the syntax is the following: (6 Task 9) --> the task will last between 6 and 9 time units. (Task 9) ( Task 9) --> the task will last between 0 and 9 time units. (6 Task ) --> the task will last between 6 time units and infinitive.

The impact factor is a dictionary of numbers and can be only positive and are cumulative. It can be defined as follows: Let's say that each task has a cost, number of workers and the hour of labour that are required to conclude the task, so each task will have an impact dictionary as this {"cost": 2, "num_workers":3, "hours": 5}". For another task the impact dictionary can be {"cost": 3, "num_workers":2, "hours": 4}.

#### Example of task with duration and impact

![Example of task with duration and impact](../src/assets/examples/taskimpacts_duration.png)

### Gateways

The gateways are used to control the flow of the process. They are used to merge or split the flow of the process. A Gateway represents an intersection where multiple paths converge or diverge. The type of gateway can be specified with the following syntax:
- Exclusive (X): splits the flow in different paths and only one is chosen given a certain condition and is indicated with a X inside the diamond. Here is also marked as orange. In our notation is defined as ^. In our notation the consition is defined as Task1 ^ Task2, where ^ is the exclusive gateway.
  - Loops are a particular type of gateways. They are used to repeat a task until a certain condition is met. Here are also marked as yellow. In our notation the consition is defined as < SomeTask >, where < ... > is the exclusive gateway.
- Parallel (+) : all the outgoing flows are followed and in the merging all the activities of the incoming flows must be completed before continuing with the process and it is indicated as + inside the diamond. Here is also marked as green. In our notation the consition is defined as Task1 || Task2, where || is the parallel gateway.

#### Example of an exclusive gateway

![Example of an exclusive gateway](../src/assets/examples/exclusive.png)

#### Example of a parallel gateway

![Example of a parallel gateway](../src/assets/examples/parallel.png)

#### Example of a loop gateway

![Example of a loop gateway](../src/assets/examples/loop.png)

### Choices for Gateways

For each type of gateway, choices depend on who or what makes the decision:

- `^` : Exclusive gateway
  - Person: Decision is made by a person with no additional notation needed.
  - Example: `Task1 ^ Task2`
  - Nature: Decision based on probability.
  - Example: `Task1 ^ [0.3]Task2` --> probability of choosing Task1 is 0.3
  - Adversary: Decision made by an adversary.
  - Example: `Task1 ^ []Task2`


- `< ... >` : Loop gateway
  - Person: the decision is taken by a person and no further notation is needed.
    - Example: `< Task1 >`
  - Nature: the decision is taken given a certain probability:
    - Example: `< [0.3]Task1 >` --> probability of choosing Task1 is 0.3 and Task2 is 0.7
  - Adversary: the decision is taken by an adversary.
    - Example: `< []Task1 >` --> the adversary will always choose for this gateway.

#### Example natural choice
![Example natural choice](../src/assets/examples/natural_xor.png)