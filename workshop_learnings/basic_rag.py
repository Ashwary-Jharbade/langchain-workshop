# import os
# from dotenv import load_dotenv
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma

# from local_llm.core import getLLM, getAgents

# load_dotenv()

# # Let's get the file's path 
# file_path = "data/HR_Support_Desk_KnowledgeBase.pdf"
# PERSIST_DIRECTORY = 'chroma_store'

# def vectorize_pdf(pdf_path: str):
#     print("======== 1. Loading PDF...")
#     # 1) Load PDF into LangChain Document format
#     loader = PyPDFLoader(pdf_path)
#     docs = loader.load()
#     print(f"Number of pages in the document: {len(docs)}")

#     #2) enrich the doc with metadata
#     print("======== 2. Enriching document with metadata...")
#     for doc in docs:
#         doc.metadata.update({
#             "source": os.path.basename(pdf_path),   # remote s3 path or local path
#             "document_name": "HR Support Desk Knowledge Base",
#             "category": "HR Policy",
#             "department": "Human Resources",
#             "document_type": "Knowledge Base",
#             "last_updated": "2024-06-01"
#         })

#     print("======== 3. Splitting document into chunks...")
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=400, # max tokens per chunk
#         chunk_overlap=50 # overlap between chunks
#     )
#     chunks = splitter.split_documents(docs)
#     print(f"===========Number of chunks created: {len(chunks)}========")

#     print("======== 4. Creating embeddings for chunks...")
#     embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

#     print("======== 5. Storing embeddings in ChromaDB vector store...")
#     vectordb = Chroma(
#       collection_name="hr_docs",
#       embedding_function=embeddings,
#       persist_directory=PERSIST_DIRECTORY
#     )

#     vectordb.add_documents(chunks)
#     print(f"======== 6. Ingested {len(chunks)} chunks into vector store.")

#     # Let's peek into the vector store -- for debugging purpose
#     results = vectordb._collection.peek(limit=1)
#     print("======== 7. Let's see vectors from the vector store:")
#     print(results)

# if __name__ == "__main__":
#     vectorize_pdf(file_path)
