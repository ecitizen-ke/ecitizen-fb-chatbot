import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA

LARGE_LANGUAGE_MODEL = os.environ["LARGE_LANGUAGE_MODEL"]
# Initialize PDF document loader
PATH = os.environ["RESOURCE_PATH"]
loader = PyPDFDirectoryLoader(PATH)


def process_docs(pdf_file):
    """
    Process the document by splitting it into chunks.
    Document splitting ensures that semantically relevant content is grouped together within the same chunk. This is particularly important when answering questions or performing other tasks that rely on the contextual information present in the documents.
    This is particularly helpful for models with limited context windows.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
    )
    return splitter.split_documents(pdf_file)


def get_text_embeddings():
    """
    Embeddings create vector representations of text, allowing us to work with text in the vector space. This is useful for semantic search, where we look for text that is most similar in the vector space.
    """
    return HuggingFaceBgeEmbeddings(
        model_name="sentence-transformers/all-MiniLM-l12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vector_store(processed_docs, embedding):
    """Store the embeddings in a database called vector stores for efficient search to retrieve the embedding vectors which are “most similar”"""
    return FAISS.from_documents(processed_docs, embedding)


def get_retriever(db, search_algorithm, no_of_doc_to_return):
    """A retriever is an interface that returns documents from the query"""
    return db.as_retriever(search_type=search_algorithm, search_kwargs={"k": no_of_doc_to_return})


def get_llm(endpoint, model, max_new_tokens, temperature):
    """"""
    return endpoint(repo_id=model, max_new_tokens=max_new_tokens, temperature=temperature)


def get_retrieval_qa(llm, retriever):
    return RetrievalQA.from_chain_type(
        retriever=retriever,
        return_source_documents=True,
        llm=llm,
        chain_type="stuff",
    )


# Load the contents of the PDF document for further processing
docs = loader.load()

text_embeddings = get_text_embeddings()


# Save text embeddings in a DB
db = get_vector_store(process_docs(docs), text_embeddings)

# Use similarity searching algorithm and retrieve 3 most relevant documents.
retriever = get_retriever(db, "similarity", 2)

llm = get_llm(HuggingFaceEndpoint, LARGE_LANGUAGE_MODEL, 256, 0.4)


def fetch_bot_response(user_input):
    """Get the model response that matches the user question"""
    qa = get_retrieval_qa(llm, retriever)
    answer = qa.invoke({"query": user_input})
    return answer["result"]
