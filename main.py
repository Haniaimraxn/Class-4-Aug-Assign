import os
import asyncio
from typing import Any, List, Optional
from agents import (
    Agent,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    RunContextWrapper,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    input_guardrail,
    output_guardrail,
)
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
from dataclasses import dataclass

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")

# Set up AI provider
provider = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

# Define models
class Account(BaseModel):
    name: str
    pin: int

class MyOutput(BaseModel):
    name: str
    balanced: str

class GuardrailAgentOutput(BaseModel):
    is_bank_related: bool

# Define agents
bank_agent = Agent(
    name='Bank Agent',
    instructions='You are a bank assistant. Help with deposits, withdrawals, and refunds, but only after confirming the customer’s identity.',
    model=model
)

result = Runner.run_sync(bank_agent, 'hi')
print(result.final_output)