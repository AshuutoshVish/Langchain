from langchain.text_splitter import CharacterTextSplitter
text = """
Artificial Intelligence (AI) enables machines to mimic human intelligence.
It powers applications like chatbots, recommendation systems, and self-driving cars.
AI learns from data to improve performance over time.
It includes fields like machine learning, computer vision, and natural language processing.
AI is transforming industries by automating tasks and enhancing decision-making.
"""

splitter = CharacterTextSplitter(chunk_size=50,
                                 chunk_overlap = 0,
                                 separator=" "
                                 )
chunkk = splitter.split_text(text)
print(chunkk[0])