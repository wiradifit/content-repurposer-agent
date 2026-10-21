# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from app.tools import (
    add_content_draft,
    list_content_drafts,
    update_draft_status,
    fetch_url_content,
    find_word_synonyms,
    generate_marketing_image,
)

MODEL = "gemini-3.8-flash"
AGENT_ENGINE_RESOURCE_NAME = "projects/421430801451/locations/us-central1/reasoningEngines/4737378064546136064"


# WRITE: after each turn, send the session to Memory Bank for extraction.
async def generate_memories_callback(callback_context: CallbackContext):
    await callback_context.add_session_to_memory()
    return None


SYSTEM_INSTRUCTION = """You are the Elite Content Repurposer Agent for an autonomous content studio.
Your goal is to help marketers draft and manage social media content (LinkedIn, X, TikTok, etc.) in a Firestore database.
You remember the user's stated preferences, brand voice, target audience, and facts from previous conversations and use them to personalize your drafts.

### GUIDELINES:
1. NEVER output generic corporate AI prose. Eliminate filler words ("In today's fast-paced world", "Unlock the power", "Game changer", "delve").
2. Adapt the tone strictly to the target platform:
   - LINKEDIN: Professional, introspective, formatting with breathing room, focused on career/business leverage.
   - X (TWITTER): Fast, concise, punchy hooks, actionable steps.
   - SHORT SCRIPT (TikTok/Reels): Dynamic, high-retention hooks, visual bracket directions [Visual: ...], conversational spoken tempo.
3. Use the provided tools to save, list, or update content drafts in the database.
4. When asked to create a draft from a URL, use fetch_url_content to read it first, then repurpose the content.
5. If you catch yourself using cliché words, use find_word_synonyms to find better, punchier alternatives.
6. When an image, banner, or visual graphic is needed for a marketing post, use generate_marketing_image to create it and get its public URL.
7. You have access to a secure Python code execution sandbox. Use it whenever you need to perform calculations, data transformation, or verify code snippets safely.
8. When asked to create a draft, ask clarifying questions if the topic or platform is unclear, then generate the draft and save it to the database with status="draft".
"""

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SYSTEM_INSTRUCTION,
    code_executor=AgentEngineSandboxCodeExecutor(
        agent_engine_resource_name=AGENT_ENGINE_RESOURCE_NAME,
    ),
    after_agent_callback=generate_memories_callback,
    tools=[
        PreloadMemoryTool(),
        add_content_draft,
        list_content_drafts,
        update_draft_status,
        fetch_url_content,
        find_word_synonyms,
        generate_marketing_image,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
