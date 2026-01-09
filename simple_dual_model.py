"""
Simple Dual-Model Assistant - Always uses both models
Gets responses from both qwen3-vl:235b-cloud and gpt-oss:120b-cloud
and presents them side by side for comparison
"""

from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def main():
    print("🤖 Initializing Dual-Model Real-Time AI Assistant...")
    print("🟡 Loading Qwen3-VL (235B Cloud)...")
    print("🔵 Loading GPT-OSS (120B Cloud)...")
    
    # Initialize both models
    qwen_model = OllamaLLM(model="qwen3-vl:235b-cloud")
    gpt_model = OllamaLLM(model="gpt-oss:120b-cloud")
    
    # Initialize search
    search = DuckDuckGoSearchRun()
    
    # Create prompts for both models
    qwen_prompt = ChatPromptTemplate.from_template("""
    You are Qwen3-VL, a multimodal AI assistant with vision capabilities.
    Use the following context from web search to answer the user's question.
    
    Context: {context}
    Question: {question}
    
    Provide a helpful answer:
    """)
    
    gpt_prompt = ChatPromptTemplate.from_template("""
    You are GPT-OSS, a powerful reasoning AI assistant.
    Use the following context from web search to answer the user's question.
    
    Context: {context}
    Question: {question}
    
    Provide a comprehensive answer:
    """)
    
    # Build chains for both models
    qwen_chain = (
        RunnablePassthrough.assign(context=lambda x: search.run(x["question"]))
        | qwen_prompt
        | qwen_model
        | StrOutputParser()
    )
    
    gpt_chain = (
        RunnablePassthrough.assign(context=lambda x: search.run(x["question"]))
        | gpt_prompt
        | gpt_model
        | StrOutputParser()
    )
    
    print("🤖 Dual-Model Assistant Ready!")
    print("🤖 I'll show you responses from both models for comparison.")
    print("🤖 Hello! What would you like to know?")
    
    while True:
        try:
            user_question = input("\nYou: ").strip()
            
            if user_question.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("🤖 Goodbye!")
                break
            
            if not user_question:
                continue
            
            print("🔍 Searching web and thinking with both models...")
            
            # Get responses from both models
            print("🟡 Getting Qwen3-VL response...")
            try:
                qwen_response = qwen_chain.invoke({"question": user_question})
            except Exception as e:
                qwen_response = f"Qwen3-VL Error: {str(e)}"
            
            print("🔵 Getting GPT-OSS response...")
            try:
                gpt_response = gpt_chain.invoke({"question": user_question})
            except Exception as e:
                gpt_response = f"GPT-OSS Error: {str(e)}"
            
            # Display both responses
            print("\n" + "="*80)
            print("🟡 QWEN3-VL RESPONSE:")
            print("-" * 40)
            print(qwen_response)
            print("\n" + "="*80)
            print("🔵 GPT-OSS RESPONSE:")
            print("-" * 40)
            print(gpt_response)
            print("="*80)
            
        except KeyboardInterrupt:
            print("\n🤖 Goodbye!")
            break
        except Exception as e:
            print(f"🤖 Sorry, I encountered an error: {str(e)}")
            print("🤖 Please try again.")

if __name__ == "__main__":
    main()