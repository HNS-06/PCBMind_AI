import json
from typing import Any
from app.core.config import get_settings

settings = get_settings()


class AIService:
    def __init__(self):
        self._groq = None
        self._gemini = None
        self._openai = None
        self._claude = None

    async def _get_groq(self):
        if self._groq is None and settings.GROQ_API_KEY:
            from groq import AsyncGroq
            self._groq = AsyncGroq(api_key=settings.GROQ_API_KEY)
        return self._groq

    async def _get_gemini(self):
        if self._gemini is None and settings.GEMINI_API_KEY:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._gemini = genai.GenerativeModel(settings.GEMINI_MODEL)
        return self._gemini

    async def _get_openai(self):
        if self._openai is None and settings.OPENAI_API_KEY:
            from openai import AsyncOpenAI
            self._openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        return self._openai

    async def _get_claude(self):
        if self._claude is None and settings.CLAUDE_API_KEY:
            import anthropic
            self._claude = anthropic.AsyncAnthropic(api_key=settings.CLAUDE_API_KEY)
        return self._claude

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str = "groq",
        temperature: float = 0.7,
        max_tokens: int = 8192,
    ) -> tuple[str, dict]:
        try:
            if model == "groq":
                return await self._generate_groq(prompt, system_prompt, temperature, max_tokens)
            elif model == "gemini":
                return await self._generate_gemini(prompt, system_prompt, temperature, max_tokens)
            elif model == "openai":
                return await self._generate_openai(prompt, system_prompt, temperature, max_tokens)
            elif model == "claude":
                return await self._generate_claude(prompt, system_prompt, temperature, max_tokens)
            else:
                raise ValueError(f"Unsupported model: {model}")
        except Exception as primary_error:
            fallbacks = {
                "groq": self._generate_gemini,
                "gemini": self._generate_groq,
            }
            if model in fallbacks:
                print(f"[AI] Primary model '{model}' failed: {primary_error}. Trying fallback...")
                try:
                    return await fallbacks[model](prompt, system_prompt, temperature, max_tokens)
                except Exception as fallback_error:
                    print(f"[AI] Fallback also failed: {fallback_error}")
            raise primary_error

    async def _generate_groq(self, prompt, system_prompt, temperature, max_tokens):
        client = await self._get_groq()
        if not client:
            raise ValueError("Groq API key not configured")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        text = response.choices[0].message.content
        tokens = {
            "input": response.usage.prompt_tokens if response.usage else 0,
            "output": response.usage.completion_tokens if response.usage else 0,
        }
        return text, tokens

    async def _generate_gemini(self, prompt, system_prompt, temperature, max_tokens):
        model = await self._get_gemini()
        if not model:
            raise ValueError("Gemini API key not configured")

        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = await model.generate_content_async(
            full_prompt,
            generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
        )
        text = response.text
        tokens = {"input": len(full_prompt.split()) * 2, "output": len(text.split()) * 2}
        return text, tokens

    async def _generate_openai(self, prompt, system_prompt, temperature, max_tokens):
        client = await self._get_openai()
        if not client:
            raise ValueError("OpenAI API key not configured")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        text = response.choices[0].message.content
        tokens = {
            "input": response.usage.prompt_tokens if response.usage else 0,
            "output": response.usage.completion_tokens if response.usage else 0,
        }
        return text, tokens

    async def _generate_claude(self, prompt, system_prompt, temperature, max_tokens):
        client = await self._get_claude()
        if not client:
            raise ValueError("Claude API key not configured")

        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt if system_prompt else "",
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text
        tokens = {
            "input": response.usage.input_tokens if response.usage else 0,
            "output": response.usage.output_tokens if response.usage else 0,
        }
        return text, tokens

    async def generate_json(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str = "groq",
        temperature: float = 0.3,
    ) -> tuple[dict, dict]:
        json_system = (
            "You must respond with valid JSON only. No markdown, no explanations, "
            "just the raw JSON object. " + (system_prompt or "")
        )
        text, tokens = await self.generate(prompt, json_system, model, temperature)
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
        return json.loads(text), tokens

    async def chat(
        self,
        message: str,
        project_context=None,
        conversation_history: list = None,
        model: str = "groq",
    ) -> tuple[str, dict]:
        system_prompt = """You are PCBMind AI, an expert electronics engineer and PCB designer.
You help users design circuits, select components, understand schematics, and optimize PCB layouts.
You can explain why specific component values are chosen, suggest alternatives, and provide
detailed technical guidance. Always be precise with electrical values and component specifications.

When discussing circuits, consider:
- Voltage and current ratings
- Power dissipation
- Component tolerances
- Temperature effects
- Signal integrity
- EMC considerations
- Cost optimization
- Availability of parts"""

        if project_context:
            proj_info = f"\n\nCurrent Project: {project_context.name}\nDescription: {project_context.description}\n"
            if project_context.components:
                proj_info += f"Components: {json.dumps(project_context.components, indent=2)}\n"
            if project_context.connections:
                proj_info += f"Connections: {json.dumps(project_context.connections, indent=2)}\n"
            system_prompt += proj_info

        messages_text = ""
        if conversation_history:
            for msg in conversation_history[-10:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                messages_text += f"\n{'User' if role == 'user' else 'Assistant'}: {content}\n"

        full_prompt = f"{messages_text}\nUser: {message}"
        return await self.generate(full_prompt, system_prompt, model)
