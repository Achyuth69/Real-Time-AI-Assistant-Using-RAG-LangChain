"""
Dual-Model Real-Time AI Assistant Using RAG + LangChain
Uses both qwen3-vl:235b-cloud and gpt-oss:120b-cloud for enhanced capabilities
- Qwen3-VL for vision and multimodal tasks
- GPT-OSS for general reasoning and text generation
"""

from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from datetime import datetime
import asyncio
import json

class DualModelRAGAssistant:
    def __init__(self):
        # Initialize both models
        self.qwen_model = OllamaLLM(model="qwen3-vl:235b-cloud")
        self.gpt_model = OllamaLLM(model="gpt-oss:120b-cloud")
        self.search = DuckDuckGoSearchRun()
        self.conversation_history = []
        
        # Prompt for model selection and coordination
        self.coordinator_prompt = ChatPromptTemplate.from_template("""
        You are a model coordinator. Analyze the user's question and determine which model(s) to use:
        
        Available models:
        - qwen3-vl:235b-cloud - Best for: vision tasks, image analysis, multimodal content, Chinese language
        - gpt-oss:120b-cloud - Best for: general reasoning, complex analysis, English text generation
        
        User question: {question}
        Search context: {context}
        
        Respond with ONLY one of these options:
        - "QWEN" - Use Qwen3-VL model only
        - "GPT" - Use GPT-OSS model only  
        - "BOTH" - Use both models and combine responses
        - "QWEN_THEN_GPT" - Use Qwen first, then GPT to refine
        """)
        
        # Qwen-specific prompt
        self.qwen_prompt = ChatPromptTemplate.from_template("""
        You are Qwen3-VL, a multimodal AI assistant with vision capabilities.
        Use the search context to provide accurate, current information.
        
        Search context: {context}
        Question: {question}
        
        Provide a helpful response:
        """)
        
        # GPT-specific prompt  
        self.gpt_prompt = ChatPromptTemplate.from_template("""
        You are GPT-OSS, a powerful reasoning AI assistant.
        Use the search context to provide detailed, analytical responses.
        
        Search context: {context}
        Question: {question}
        
        Provide a comprehensive response:
        """)
        
        # Combination prompt
        self.combination_prompt = ChatPromptTemplate.from_template("""
        You are combining responses from two AI models. Create a unified, coherent answer.
        
        Original question: {question}
        Search context: {context}
        
        Qwen3-VL response: {qwen_response}
        GPT-OSS response: {gpt_response}
        
        Combine these responses into a single, comprehensive answer:
        """)
    
    def search_with_error_handling(self, question):
        """Search with error handling"""
        try:
            results = self.search.run(question)
            return results
        except Exception as e:
            return f"Search unavailable: {str(e)}. Using model knowledge only."
    
    def determine_model_strategy(self, question, context):
        """Determine which model(s) to use"""
        try:
            coordinator_chain = self.coordinator_prompt | self.gpt_model | StrOutputParser()
            strategy = coordinator_chain.invoke({
                "question": question,
                "context": context
            }).strip().upper()
            
            # Fallback to GPT if strategy is unclear
            if strategy not in ["QWEN", "GPT", "BOTH", "QWEN_THEN_GPT"]:
                strategy = "GPT"
                
            return strategy
        except Exception as e:
            print(f"⚠️ Strategy determination failed: {e}")
            return "GPT"  # Fallback
    
    def get_qwen_response(self, question, context):
        """Get response from Qwen3-VL model"""
        try:
            qwen_chain = self.qwen_prompt | self.qwen_model | StrOutputParser()
            return qwen_chain.invoke({"question": question, "context": context})
        except Exception as e:
            return f"Qwen model error: {str(e)}"
    
    def get_gpt_response(self, question, context):
        """Get response from GPT-OSS model"""
        try:
            gpt_chain = self.gpt_prompt | self.gpt_model | StrOutputParser()
            return gpt_chain.invoke({"question": question, "context": context})
        except Exception as e:
            return f"GPT model error: {str(e)}"
    
    def combine_responses(self, question, context, qwen_response, gpt_response):
        """Combine responses from both models"""
        try:
            combination_chain = self.combination_prompt | self.gpt_model | StrOutputParser()
            return combination_chain.invoke({
                "question": question,
                "context": context,
                "qwen_response": qwen_response,
                "gpt_response": gpt_response
            })
        except Exception as e:
            # Fallback: simple concatenation
            return f"**Combined Response:**\n\n**Qwen3-VL:** {qwen_response}\n\n**GPT-OSS:** {gpt_response}"
    
    def process_question(self, question):
        """Main processing logic using both models"""
        print("🔍 Searching web...")
        context = self.search_with_error_handling(question)
        
        print("🤖 Determining optimal model strategy...")
        strategy = self.determine_model_strategy(question, context)
        print(f"📋 Strategy: {strategy}")
        
        if strategy == "QWEN":
            print("🟡 Using Qwen3-VL model...")
            response = self.get_qwen_response(question, context)
            model_info = "**Model Used:** Qwen3-VL"
            
        elif strategy == "GPT":
            print("🔵 Using GPT-OSS model...")
            response = self.get_gpt_response(question, context)
            model_info = "**Model Used:** GPT-OSS"
            
        elif strategy == "BOTH":
            print("🟡 Getting Qwen3-VL response...")
            qwen_response = self.get_qwen_response(question, context)
            print("🔵 Getting GPT-OSS response...")
            gpt_response = self.get_gpt_response(question, context)
            print("🔄 Combining responses...")
            response = self.combine_responses(question, context, qwen_response, gpt_response)
            model_info = "**Models Used:** Qwen3-VL + GPT-OSS (Combined)"
            
        elif strategy == "QWEN_THEN_GPT":
            print("🟡 Getting Qwen3-VL response...")
            qwen_response = self.get_qwen_response(question, context)
            print("🔵 Refining with GPT-OSS...")
            refined_context = f"Previous analysis: {qwen_response}\n\nOriginal context: {context}"
            response = self.get_gpt_response(question, refined_context)
            model_info = "**Models Used:** Qwen3-VL → GPT-OSS (Sequential)"
        
        return f"{model_info}\n\n{response}"
    
    def add_to_history(self, question, answer):
        """Add to conversation history"""
        timestamp = datetime.now().strftime("%H:%M")
        self.conversation_history.extend([
            f"[{timestamp}] {question}",
            f"[{timestamp}] {answer[:300]}..."  # Truncate for history
        ])
        
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def save_conversation(self, filename="dual_model_conversation.json"):
        """Save conversation to file"""
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "models_used": ["qwen3-vl:235b-cloud", "gpt-oss:120b-cloud"],
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
        print("🤖 Dual-Model Real-Time AI Assistant is ready!")
        print("🟡 Qwen3-VL: Vision, multimodal, Chinese language")
        print("🔵 GPT-OSS: General reasoning, complex analysis")
        print("🔄 Smart model selection and combination")
        print("📋 Commands: 'exit', 'save', 'clear', 'models'")
        print("\n🤖 Hello! I can use both models to give you the best answers. What would you like to know?")
        
        while True:
            try:
                user_question = input("\nYou: ").strip()
                
                if user_question.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("🤖 Goodbye! Thanks for using the dual-model assistant!")
                    break
                
                if user_question.lower() == 'save':
                    self.save_conversation()
                    continue
                
                if user_question.lower() in ['clear', 'clear history']:
                    self.conversation_history = []
                    print("🤖 Conversation history cleared!")
                    continue
                
                if user_question.lower() == 'models':
                    print("🟡 Qwen3-VL: qwen3-vl:235b-cloud - Vision, multimodal tasks")
                    print("🔵 GPT-OSS: gpt-oss:120b-cloud - General reasoning, analysis")
                    continue
                
                if not user_question:
                    continue
                
                # Process with dual models
                response = self.process_question(user_question)
                
                # Add to history and display
                self.add_to_history(user_question, response)
                print(f"\n🤖: {response}")
                
            except KeyboardInterrupt:
                print("\n🤖 Goodbye!")
                break
            except Exception as e:
                print(f"🤖 Sorry, I encountered an error: {str(e)}")
                print("🤖 Please try again.")

def main():
    assistant = DualModelRAGAssistant()
    assistant.run()

if __name__ == "__main__":
    main()