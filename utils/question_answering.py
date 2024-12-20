from typing import Annotated, Generator
from typing_extensions import TypedDict
from langchain_mistralai import ChatMistralAI
from langchain import hub
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_community.utilities import SQLDatabase
from langgraph.graph import START, StateGraph
from functools import partial

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State, db: SQLDatabase, llm: ChatMistralAI):
    """Generate SQL query to fetch information and update the state with the query.
    :param state: State - The current state of the conversation.
    :param db: SQLDatabase - The database to query.
    :param llm: ChatMistralAI - The language model to use for generating the query.
    :return: Dict[str, str] - The generated SQL query.
    """
    prompt = hub.pull("langchain-ai/sql-query-system-prompt").invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )

    print(prompt)

    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}

def execute_query(state: State, db: SQLDatabase):
    """Execute SQL query and update the state with the result.
    :param state: State - The current state of the conversation.
    :param db: SQLDatabase - The database to query.
    :return: Dict[str, str] - The result of the query.
    """
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

def generate_answer(state: State, llm: ChatMistralAI):
    """Answer question using retrieved information as context.
    :param state: State - The current state of the conversation.
    :param llm: ChatMistralAI - The language model to use for question answering.
    :return: Dict[str, str] - The answer to the question.
    """
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )

    if not state["result"]:
        prompt = (
            "Given the following user question, "
            "say that you don't have or did not find the information to answer the user question.\n\n"
            f'Question: {state["question"]}\n'
        )
    else:
        prompt = (
            "Given the following user question, corresponding SQL query, "
            "and SQL result, answer the user question.\n\n"
            f'Question: {state["question"]}\n'
            f'SQL Query: {state["query"]}\n'
            f'SQL Result: {state["result"]}'
        )

    print(prompt)

    response = llm.invoke(prompt)
    return {"answer": response.content}

def get_graph(db: SQLDatabase, llm: ChatMistralAI) -> StateGraph:
    """Create the state graph for the question answering pipeline.
    :param db: SQLDatabase - The database to query.
    :param llm: ChatMistralAI - The language model to use for question answering.
    :return: StateGraph - The state graph for the question answering pipeline.
    """

    graph_builder = StateGraph(State)
    
    graph_builder.add_node("write_query", partial(write_query, db=db, llm=llm))
    graph_builder.add_node("execute_query", partial(execute_query, db=db))
    graph_builder.add_node("generate_answer", partial(generate_answer, llm=llm))

    graph_builder.add_edge(START, "write_query")
    graph_builder.add_edge("write_query", "execute_query")
    graph_builder.add_edge("execute_query", "generate_answer")
    return graph_builder.compile()

def answer_question(graph: StateGraph, question: str) -> Generator[str, None, None]:
    """Answer a question using the question answering pipeline.
    :param graph: StateGraph - The state graph for the question answering pipeline.
    :param question: str - The question to answer.
    :return: Generator[str, None, None] - The answer to the question.
    """
    
    for message, metadata in graph.stream({"question": question}, stream_mode="messages"):
        if metadata['langgraph_node'] == 'generate_answer':
            yield message.content

    




