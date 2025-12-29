from langchain_text_splitters import RecursiveCharacterTextSplitter

text_spliter=RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=20,separators=[" ","\n","\n\n"])
text=["""Artificial Intelligence (AI) is a branch of computer science that focuses on creating systems capable of performing tasks that normally require human intelligence. These tasks include learning from data, recognizing patterns, understanding natural language, and making decisions.

Machine Learning is a subset of Artificial Intelligence. It allows computers to learn automatically from past experiences without being explicitly programmed. Common machine learning techniques include supervised learning, unsupervised learning, and reinforcement learning.

Deep Learning is a specialized area within Machine Learning that uses neural networks with multiple layers. These models are particularly effective in image recognition, speech processing, and natural language understanding. Convolutional Neural Networks and Recurrent Neural Networks are popular deep learning architectures.""" ]


docs=text_spliter.create_documents(text)
doc=docs[0]
for i,doc in enumerate(docs):
    print(f"-----chunk-------{i+1}")
    print("content",doc.page_content)