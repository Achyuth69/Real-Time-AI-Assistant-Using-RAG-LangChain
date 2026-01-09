"""
Advanced Real-Time AI Assistant with Enhanced Features
This version includes additional features like conversation history,
source citations, and better error handling.
"""

from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from datetime import datetime
import json

class AdvancedRAGAssistant:
    def __init__(self, model_name="gpt-oss:120b-cloud"):
        self.llm = OllamaLLM(model=model_name)
        self.search = DuckDuckGoSearchRun()
        self.conversation_history = []
        
        # Enhanced prompt with source citation
        self.prompt = ChatPromptTemplate.from_template("""
        You are a helpful AI assistant with access to real-time information.
        Use the following context from web search results to answer the user's question.
        
        IMPORTANT: 
        - If you use information from the search results, mention that it's from recent web search
        - Be specific about what information comes from search vs your training knowledge
        - If the search results don't contain relevant information, rely on your general knowledge
        
        Previous conversation context:
        {history}
        
        Current web search results:
        {context}
        
        Current question: {question}
        
        Provide a helpful, accurate answer:
        """)
        
        # Build the enhanced chain
        self.chain = (
            RunnablePassthrough.assign(
                context=lambda x: self.search_with_error_handling(x["question"]),
                history=lambda x: self.format_history()
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def search_with_error_handling(self, question):
        """Search with better error handling"""
        try:
            results = self.search.run(question)
            return results
        except Exception as e:
            return f"Search unavailable: {str(e)}. Using general knowledge only."
    
    def format_history(self):
        """Format recent conversation history"""
        if not self.conversation_history:
            return "No previous conversation."
        
        # Keep last 3 exchanges to avoid context overflow
        recent_history = self.conversation_history[-6:]  # 3 Q&A pairs
        formatted = []
        
        for i in range(0, len(recent_history), 2):
            if i + 1 < len(recent_history):
                q = recent_history[i]
                a = recent_history[i + 1]
                formatted.append(f"Q: {q}\nA: {a[:200]}...")  # Truncate long answers
        
        return "\n\n".join(formatted)
    
    def add_to_history(self, question, answer):
        """Add Q&A to conversation history"""
        timestamp = datetime.now().strftime("%H:%M")
        self.conversation_history.extend([
            f"[{timestamp}] {question}",
            f"[{timestamp}] {answer}"
        ])
        
        # Keep history manageable (last 20 entries)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def save_conversation(self, filename="conversation_log.json"):
        """Save conversation to file"""
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "history": self.conversation_history
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Conversation saved to {filename}")
        except Exception as e:
            print(f"❌ Could not save conversation: {e}")
    
    def run(self):
        """Main interactive loop"""
        print("🤖 Advanced Real-Time AI Assistant is ready!")
        print("🤖 Features: Web search, conversation memory, source citations")
        print("🤖 Commands: 'exit', 'save', 'clear history'")
        print("🤖 Hello! What would you like to know?")
        
        while True:
            try:
                user_question = input("\nYou: ").strip()
                
                # Handle special commands
                if user_question.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("🤖 Goodbye! Thanks for chatting!")
                    break
                
                if user_question.lower() == 'save':
                    self.save_conversation()
                    continue
                
                if user_question.lower() in ['clear history', 'clear']:
                    self.conversation_history = []
                    print("🤖 Conversation history cleared!")
                    continue
                
                if not user_question:
                    continue
                
                print("🤖 Searching and thinking...")
                
                # Get response from the chain
                response = self.chain.invoke({"question": user_question})
                
                # Add to history and display
                self.add_to_history(user_question, response)
                print(f"🤖: {response}")
                
            except KeyboardInterrupt:
                print("\n🤖 Goodbye!")
                break
            except Exception as e:
                print(f"🤖 Sorry, I encountered an error: {str(e)}")
                print("🤖 Please try again.")

def main():
    # You can change the model here
    assistant = AdvancedRAGAssistant(model_name="gpt-oss:120b-cloud")
    assistant.run()

if __name__ == "__main__":
    main()