from langchain.base_language import BaseLanguageModel
from langchain.callbacks.base import BaseCallbackManager
from langchain.chat_models.base import BaseChatModel
from toolemu.agents import (
    SIMULATORS,
    AgentExecutorWithToolkit,
    ZeroShotAgentWithToolkit,
)
from toolemu.tools import get_toolkits_by_names
from toolemu.utils.my_typing import *
from typing import Any

def build_agent_executor(
    toolkits: List[str],
    agent_llm: BaseLanguageModel,
    simulator_llm: BaseLanguageModel,
    critiquer_llm: Optional[BaseLanguageModel] = None,
    num_critique_steps: int = 0,
    max_allowed_steps: int = 3,
    agent_type: str = "helpful_ss",
    simulator_type: str = "std_thought",
    verbose: bool = True,
    return_intermediate_steps: bool = True,
    max_iterations: int = 15,
    
    mcp_defense_tok: Optional[Any] = None,
    mcp_defense_model: Optional[Any] = None,
    
    callback_manager: Optional[BaseCallbackManager] = None,
) -> Type[AgentExecutorWithToolkit]:
    toolkits = get_toolkits_by_names(toolkits)
    agent = ZeroShotAgentWithToolkit.from_llm_and_toolkits(
        toolkits=toolkits,
        llm=agent_llm,
        agent_type=agent_type,
        use_chat_format=isinstance(agent_llm, BaseChatModel),
    )
    executor_class = SIMULATORS[simulator_type]
    if simulator_type != "normal":
        agent_executer = executor_class.from_agent_and_toolkits(
            toolkits=toolkits,
            agent=agent,
            verbose=verbose,
            llm_simulator=simulator_llm,
            llm_critiquer=critiquer_llm,
            num_critique_steps=num_critique_steps,
            max_allowed_steps=max_allowed_steps,
            use_chat_format=isinstance(simulator_llm, BaseChatModel),
            return_intermediate_steps=return_intermediate_steps,
            max_iterations=max_iterations,
            callback_manager=callback_manager,
            
            mcp_defense_tok=mcp_defense_tok,
            mcp_defense_model=mcp_defense_model,
        )
    else:
        agent_executer = executor_class.from_agent_and_toolkits(
            toolkits=toolkits,
            agent=agent,
            verbose=verbose,
            max_iterations=max_iterations,
            callback_manager=callback_manager,
        )
    return agent_executer
