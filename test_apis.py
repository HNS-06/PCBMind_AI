"""
Quick API Test Script - Verifies Groq and Gemini API connectivity.
Run: py test_apis.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))

# Import API keys from environment variables
from os import environ


async def test_groq():
    print("=" * 50)
    print("Testing Groq API (llama-3.1-8b-instant)")
    print("=" * 50)
    try:
        from groq import AsyncGroq
        client = AsyncGroq(api_key=environ["GROQ_API_KEY"])

        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful electronics engineer."},
                {"role": "user", "content": "What is the formula for calculating resistor value for an LED? Reply in 2 sentences."},
            ],
            temperature=0.7,
            max_tokens=100,
        )
        text = response.choices[0].message.content
        tokens_in = response.usage.prompt_tokens
        tokens_out = response.usage.completion_tokens
        print(f"Response: {text[:200]}")
        print(f"Tokens: {tokens_in} in, {tokens_out} out")
        print("Groq API: OK")
        return True
    except Exception as e:
        print(f"Groq API ERROR: {e}")
        return False


async def test_gemini():
    gemini_model = environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    print("\n" + "=" * 50)
    print(f"Testing Gemini API ({gemini_model})")
    print("=" * 50)
    try:
        import google.generativeai as genai
        genai.configure(api_key=environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel(gemini_model)

        response = await model.generate_content_async(
            "What is Ohm's law? Reply in 1 sentence.",
            generation_config={"temperature": 0.7, "max_output_tokens": 50},
        )
        text = response.text
        print(f"Response: {text[:200]}")
        print("Gemini API: OK")
        return True
    except Exception as e:
        print(f"Gemini API ERROR: {e}")
        return False


async def main():
    print("\nPCBMind AI - API Connectivity Test\n")
    groq_ok = await test_groq()
    gemini_ok = await test_gemini()

    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"Groq:  {'PASS' if groq_ok else 'FAIL'}")
    print(f"Gemini: {'PASS' if gemini_ok else 'FAIL'}")

    if groq_ok or gemini_ok:
        print("\nAt least one API is working. PCBMind AI is ready!")
    else:
        print("\nNo APIs working. Check your keys and network.")
    print()


if __name__ == "__main__":
    asyncio.run(main())
