"""
Real-Time AI Assistant Using RAG + LangChain
A powerful AI assistant that can search the web and answer questions in real-time
using open-source tools: Ollama + LangChain + DuckDuckGo Search
Now powered by GPT-OSS 120B Cloud model for enhanced performance
"""

from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def main():
    print("🤖 Initializing Real-Time AI Assistant...")
    
    # Initialize the LLM (GPT-OSS 120B via Ollama)
    llm = OllamaLLM(model="gpt-oss:120b-cloud")
    
    # Initialize the search tool (DuckDuckGo)
    search = DuckDuckGoSearchRun()
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful AI assistant with access to real-time information.
    Use the following context from web search results to answer the user's question.
    If the context doesn't contain relevant information, say so and provide your best general knowledge answer.
    
    Context from web search:
    {context}
    
    Question: {question}
    
    Answer:
    """)
    
    # Build the RAG chain using LCEL (LangChain Expression Language)
    # This chain:
    # 1. Takes the input question
    # 2. Searches the web for relevant information
    # 3. Passes both the question and search results to the LLM
    # 4. Returns the LLM's response
    chain = (
        RunnablePassthrough.assign(context=lambda x: search.run(x["question"]))
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("🤖 Real-Time AI Assistant is ready!")
    print("🤖 Hello! I'm a real-time AI assistant. What's new?")
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_question = input("You: ").strip()
            
            # Check for exit commands
            if user_question.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("🤖 Goodbye!")
                break
            
            if not user_question:
                continue
            
            print("🤖 Thinking...")
            
            # Run the chain with the user's question
            response = chain.invoke({"question": user_question})
            
            print(f"🤖: {response}")
            print()
            
        except KeyboardInterrupt:
            print("\n🤖 Goodbye!")
            break
        except Exception as e:
            print(f"🤖 Sorry, I encountered an error: {str(e)}")
            print("🤖 Please try again.")

if __name__ == "__main__":
    main()