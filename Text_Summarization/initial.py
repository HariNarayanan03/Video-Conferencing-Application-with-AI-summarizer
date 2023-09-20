#
#
# from  transformers import pipeline
# from pdfminer.high_level import extract_text
# import docx2txt
#
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#
# def txt_ext(f):
#     if f.endswith(".pdf"):
#         return extract_text(f)
#     else:
#         res_txt= docx2txt.process(f)
#     if res_txt:
#         return res_txt.replace('\t',' ')
#     return None
#
# if __name__ == '__bart__':
#     # txt = txt_ext('sample.pdf')
#     txt="India, officially the Republic of India (ISO: Bhārat Gaṇarājya),[21] is a country in South Asia. It is the seventh-largest country by area; the most populous country as of June 2023;[22][23] and from the time of its independence in 1947, the world's most populous democracy.[24][25][26] Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west;[j] China, Nepal, and Bhutan to the north; and Bangladesh and Myanmar to the east. In the Indian Ocean, India is in the vicinity of Sri Lanka and the Maldives; its Andaman and Nicobar Islands share a maritime border with Thailand, Myanmar, and Indonesia. Modern humans arrived on the Indian subcontinent from Africa no later than 55,000 years ago.[27][28][29] Their long occupation, initially in varying forms of isolation as hunter-gatherers, has made the region highly diverse, second only to Africa in human genetic diversity.[30] Settled life emerged on the subcontinent in the western margins of the Indus river basin 9,000 years ago, evolving gradually into the Indus Valley Civilisation of the third millennium BCE.[31] By 1200 BCE, an archaic form of Sanskrit, an Indo-European language, had diffused into India from the northwest.[32][33] Its evidence today is found in the hymns of the Rigveda. Preserved by an oral tradition that was resolutely vigilant, the Rigveda records the dawning of Hinduism in India.[34] The Dravidian languages of India were supplanted in the northern and western regions.[35] By 400 BCE, stratification and exclusion by caste had emerged within Hinduism,[36] and Buddhism and Jainism had arisen, proclaiming social orders unlinked to heredity.[37] Early political consolidations gave rise to the loose-knit Maurya and Gupta Empires based in the Ganges Basin.[38] Their collective era was suffused with wide-ranging creativity,[39] but also marked by the declining status of women,[40] and the incorporation of untouchability into an organised system of belief.[k][41] In South India, the Middle kingdoms exported Dravidian-languages scripts and religious cultures to the kingdoms of Southeast Asia"
#     # print(txt[:504])
#     print(len(txt))
#     word_max = (int)(len(txt)*0.75)
#     print("MAX",word_max)
#     word_min = (int)(len(txt)*0.45)
#     print("MIN",word_min)
#     summary = summarizer(txt, max_length=425, min_length=350, do_sample=False)
#     print(len(summary))
#     print("The summary extracted is:", summary)
#     print("END")
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
