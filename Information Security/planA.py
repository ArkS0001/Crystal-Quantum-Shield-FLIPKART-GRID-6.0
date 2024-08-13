from transformers import pipeline
folder_dir = "CyBERTuned"
unmasker = pipeline('fill-mask', model=folder_dir)
unmasker("RagnarLocker, LockBit, and REvil are types of <mask>.")


# text requiring url comprehension (redirection attack), modified from https://intezer.com/blog/research/targeted-phishing-attack-against-ukrainian-government-expands-to-georgia/
url_text = 'The PDF contains an action object. Upon a victim opening the PDF it will send a query to Google: http://www[.]google[.]com/url?q=http%3A%2F%2F9348243249382479234343284324023432748892349702394023.xyz&sa=D&sntz=1&usg=AFQjCNFWmVffgSGlrrv-2U9sSOJYzfUQqw. This link is a typical <mask> attack.'
unmasker(url_text)[0]


from transformers import AutoModel, AutoTokenizer
model = AutoModel.from_pretrained(folder_dir)
tokenizer = AutoTokenizer.from_pretrained(folder_dir)
text = "Cybersecurity information is often technically complex and relayed through unstructured text, making automation of cyber threat intelligence highly challenging."
encoded = tokenizer(text, return_tensors="pt")
output = model(**encoded)
output[0].shape
