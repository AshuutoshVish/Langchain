from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path = "raw.csv")
data=loader.load()
print(data[0])