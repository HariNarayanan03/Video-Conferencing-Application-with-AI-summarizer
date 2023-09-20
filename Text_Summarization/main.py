import torch
import transformers
from transformers import BartTokenizer, BartForConditionalGeneration

tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn',truncation=True)
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

torch_device = 'cpu'


def bart_summarize(text, num_beams, length_penalty, max_length, min_length, no_repeat_ngram_size):
    text = text.replace('\n', '')
    text_input_ids = tokenizer.batch_encode_plus([text], return_tensors='pt', max_length=1024)['input_ids'].to(
        torch_device)
    summary_ids = model.generate(text_input_ids, num_beams=int(num_beams), length_penalty=float(length_penalty),
                                 max_length=int(max_length), min_length=int(min_length),
                                 no_repeat_ngram_size=int(no_repeat_ngram_size))
    summary_txt = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
    return summary_txt


if __name__ == '__main__':

    txt="India, officially the Republic of India (ISO: Bhārat Gaṇarājya),[21] is a country in South Asia. It is the seventh-largest country by area; the most populous country as of June 2023;[22][23] and from the time of its independence in 1947, the world's most populous democracy.[24][25][26] Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west;[j] China, Nepal, and Bhutan to the north; and Bangladesh and Myanmar to the east. In the Indian Ocean, India is in the vicinity of Sri Lanka and the Maldives; its Andaman and Nicobar Islands share a maritime border with Thailand, Myanmar, and Indonesia. Modern humans arrived on the Indian subcontinent from Africa no later than 55,000 years ago.[27][28][29] Their long occupation, initially in varying forms of isolation as hunter-gatherers, has made the region highly diverse, second only to Africa in human genetic diversity.[30] Settled life emerged on the subcontinent in the western margins of the Indus river basin 9,000 years ago, evolving gradually into the Indus Valley Civilisation of the third millennium BCE.[31] By 1200 BCE, an archaic form of Sanskrit, an Indo-European language, had diffused into India from the northwest.[32][33] Its evidence today is found in the hymns of the Rigveda. Preserved by an oral tradition that was resolutely vigilant, the Rigveda records the dawning of Hinduism in India.[34] The Dravidian languages of India were supplanted in the northern and western regions.[35] By 400 BCE, stratification and exclusion by caste had emerged within Hinduism,[36] and Buddhism and Jainism had arisen, proclaiming social orders unlinked to heredity.[37] Early political consolidations gave rise to the loose-knit Maurya and Gupta Empires based in the Ganges Basin.[38] Their collective era was suffused with wide-ranging creativity,[39] but also marked by the declining status of women,[40] and the incorporation of untouchability into an organised system of belief.[k][41] In South India, the Middle kingdoms exported Dravidian-languages scripts and religious cultures to the kingdoms of Southeast Asia"
    print(len(txt))
    word_max = (int)(len(txt) * 0.75)
    print("MAX", word_max)
    word_min = (int)(len(txt) * 0.45)
    print("MIN", word_min)
    sum=bart_summarize(txt,4,2,word_max,word_min,3)
    print("Summary: ",sum)