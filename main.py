import os  
from langchain_community.document_loaders import PyPDFLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel , RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_community.docstore.document import Document
import requests.exceptions
import pandas as pd



def load_excel_file(file_path):
    
    print("Loading Excel File")
    
    try:
        df = pd.read_excel(file_path)
        
        print(f"Excel file structure:")
        print(f"- Number of rows: {len(df)}")
        print(df.info())
        
        documents = []
        
        for i , row in df.iterrows():
            
            content = f"Employee Record:\n"
            content += f"Nmae : {row['Name']}\n"
            content += f"Postion : {row['Position']}\n"
            content += f"Department: {row['Department']}\n"
            content += f"Gender  : {row['Gender']}\n"
            content += f"Vacation Days Taken: {row['Vacation Taken']}\n"
            content += f"Sick Leaves Taken: {row['Sick Leaves']}\n"

            doc = Document(
                page_content = content,
                metadata={
                    "source":file_path,
                    "row_index" : i,
                    "employee_name":row['Name']
                    }
                )
            documents.append(doc)
            
        print(f"Successfully created {len(documents)} documents from Excel rows")
        return documents
    
    except Exception as e:
        print(f"Error While Processing Excel File")
        return e


excel_docs = load_excel_file("employee_list.xlsx")

pdf_loader = PyPDFLoader("CompanyVacationPolicy.pdf")

# Load Documents 
try:
    pdf_docs = pdf_loader.load()
    print("PDF loaded successfully")
except Exception as e:
    print(e)


documents = excel_docs + pdf_docs


embeddings = OllamaEmbeddings(model="all-minilm")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200, 
    length_function=len
    )

splits = text_splitter.split_documents(documents)
print(f"Text Chunks lenght {len(splits)}")


print("Creating vector store...")
vectorstore = FAISS.from_documents(
        documents= splits,
        embedding= embeddings
    )

vectorstore.save_local("faiss_index")
print("Vector store created and saved")


llm = OllamaLLM(
    model="llama3.2",
    temperature=0.1
    )


template = """Answer the following question based on the provided context. Follow these rules:

1. Answer the question using ONLY one short sentence.
2. If the question is about vacation days, return only the remaining vacation days.
3. For questions about specific employees, clearly state:
   - Their position and department
   - Number of vacation days taken
   - Number of vacation days remaining (25 minus days taken)
4. If looking at historical data, mention when we don't have the full year's context.
5. If the employee name in the question does NOT appear in the context,
   respond exactly with:
   "The employee does not exist in the available records."
   Do not invent or guess employee information.

Context: {context}

Question: {question}

Answer using ONLY the information from the context. If the context does not contain the answer,
say "I cannot answer this question based on the available information."

Answer:"""

prompt = PromptTemplate(
    template = template,
    input_variables=["context", "question"]
    )


retriever = vectorstore.as_retriever(search_kwargs={'k':3})

rag_chain = (
    {"context":retriever , "question":RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()    
)

def query_documents(question : str):
    try:
        return rag_chain.invoke(question)
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama. Please make sure the Ollama service is running."
    except Exception as e:
        return f"Error: {str(e)}"




