# COMMENTED OUT - Not needed for foundation (API connection verification)
# from gemini_client import GeminiClient
# import os

# def verify():
#     print("Initializing Gemini Client...")
#     try:
#         client = GeminiClient()
#         print("✅ Client initialized successfully.")
#     except Exception as e:
#         print(f"❌ Failed to initialize client: {e}")
#         return

#     # List available models
#     print("Listing available models...")
#     try:
#         for m in genai.list_models():
#             if 'generateContent' in m.supported_generation_methods:
#                 print(f"Found model: {m.name}")
#     except Exception as e:
#         print(f"❌ Failed to list models: {e}")

#     # Simple text generation check
#     print("Testing basic text generation with gemini-pro (fallback)...")
#     try:
#         # constant fallback for test
#         model = genai.GenerativeModel('gemini-pro') 
#         response = model.generate_content("Hello")
#         print(f"✅ API Response received: {response.text}")
#     except Exception as e:
#          print(f"❌ API Call failed on fallback: {e}")

# if __name__ == "__main__":
#     verify()
