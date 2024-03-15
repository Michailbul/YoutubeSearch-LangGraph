import os, openai
from langchain import hub
from langchain_community.tools import YouTubeSearchTool
from langchain.agents import create_openai_functions_agent
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.agents import AgentFinish
import streamlit as st
import sys
import dotenv
from langgraph.graph import END, Graph
from dotenv import load_dotenv, find_dotenv


#sys.path.append('../..')
#openai_api_key = os.environ['OPENAI_API_KEY']

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

#TODO add memory to chat with it

def app_initialize(openai_api_key):


    prompt = hub.pull("hwchase17/openai-functions-agent")

    llm = ChatOpenAI(model='gpt-3.5-turbo')
    """
    YouTube Search package searches YouTube videos avoiding using their heavily rate-limited API.

    It uses the form on the YouTube homepage and scrapes the resulting page.

    """
    tools = [YouTubeSearchTool()]


    agent_runnable = create_openai_functions_agent(llm, tools, prompt=prompt)

    agent = RunnablePassthrough.assign(agent_outcome = agent_runnable)


    def tool_function(data):
        agent_action = data.pop('agent_outcome')
        tool_to_use = {t.name: t for t in tools}[agent_action.tool]
        observation = tool_to_use.invoke(agent_action.tool_input)
        data['intermediate_steps'].append((agent_action, observation))
        print(data)
        return data



    def should_continue(data):
        if isinstance(data['agent_outcome'], AgentFinish):
            return "end"
        else:
            return "continue"
        

    workflow = Graph()

    workflow.add_node('agent', agent)
    workflow.add_node('tools', tool_function)

    workflow.set_entry_point('agent')

    workflow.add_conditional_edges('agent',
        should_continue,
        {
        'continue': 'tools',
        'end' : END
        }
    )

    workflow.add_edge('tools', 'agent' )

    app = workflow.compile()
    
    return app



#app = app_initialize(openai_api_key)

with st.sidebar:
    openai_api_key = st.text_input('Your OpenAI API key', key ='chatbot_api_key', type='password')
    
st.title ('💬 Search Youtube')
st.caption("🚀 A streamlit agent powered by OpenAI LLM to search Youtube")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

app = app_initialize(openai_api_key)

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
 
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
   
    result = app.invoke({"input": prompt, "intermediate_steps": []})
    msg = result['agent_outcome'].return_values["output"]
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)