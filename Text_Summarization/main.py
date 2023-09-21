import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import torch
import transformers
import flask
from flask import Flask,request,Response,jsonify
from transformers import BartTokenizer, BartForConditionalGeneration

tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn',truncation=True)
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

torch_device = 'cpu'

app= Flask(__name__)

@app.route('/',methods=['GET'])
def chk():
    return "HIIIII",200
@app.route('/summarize',methods=['GET','POST'])
def call():
    print("HIII Mail")
    form=request.form.to_dict()
    txt=form['txt']
    print(len(txt))
    word_max = (int)(len(txt) * 0.15)
    print("MAX", word_max)
    word_min = (int)(len(txt) * 0.10)
    print("MIN", word_min)
    sum = bart_summarize(txt, 4, 2, word_max, word_min, 3)
    print("Summary: ", sum)
    toaddr = form['to']
    msg = MIMEMultipart()
    msg['From'] = '2012070@nec.edu.in'
    msg['To'] = toaddr
    msg['Subject'] = "Summarization made for the meeting"
    body = "Summarization of the meeting was attached\n\n"+sum
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('2012070@nec.edu.in', "Nechuvan@3002")
    text = msg.as_string()
    # if (len(toaddr) < 6):
    s.sendmail('2012070@nec.edu.in', toaddr, text)
    s.quit()
    return sum,200
def bart_summarize(text, num_beams, length_penalty, max_length, min_length, no_repeat_ngram_size):
    text = text.replace('\n', '')
    print("1")
    text_input_ids = tokenizer.batch_encode_plus([text], return_tensors='pt', max_length=1024)['input_ids'].to(
        torch_device)
    print("2")
    summary_ids = model.generate(text_input_ids, num_beams=int(num_beams), length_penalty=float(length_penalty),
                                 max_length=int(max_length), min_length=int(min_length),
                                 no_repeat_ngram_size=int(no_repeat_ngram_size))
    print("3")
    summary_txt = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
    print("4")
    return summary_txt


if __name__ == '__main__':

    app.run(debug=True)
    # txt="It turns out Facebook is only guilty of about half of what it’s been accused of in the gay kiss incident. The social networking site apologized yesterday for taking down an image used to promote a “kiss-in” event in London. “The photo in question does not violate our Statement of Rights and Responsibilities, and was removed in error,” the site said in a statement, according to the Advocate. But Facebook did not, as has been reported in several places, take down the kiss-in event itself. Here’s what happened: The photo Facebook took down was posted by the Dangerous Minds blog to promote the event. In its initial write-up about the incident, the blog observed that the page organizing the protest had been taken down. But it was actually the organizer himself who removed the event, Dangerous Minds clarified. Organizer Paul Shetler explains that he decided to switch it from a public event to a private one, as there were starting to be trolls posting abusive nonsense on it."
    # print(len(txt))
    # word_max = (int)(len(txt) * 0.15)
    # print("MAX", word_max)
    # word_min = (int)(len(txt) * 0.10)
    # print("MIN", word_min)
    # sum=bart_summarize(txt,4,2,word_max,word_min,3)
    # print("Summary: ",sum)