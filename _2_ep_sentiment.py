from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentimentAnalyser = SentimentIntensityAnalyzer()

import pandas as pd
pd.options.display.max_colwidth = 400

import nltk
nltk.download('punkt')

transcript = open("[transcription file pathname]").read()

nltk.sent_tokenize(transcript)

for number, sentence in enumerate(nltk.sent_tokenize(transcript)):
    print(number, sentence)

# Break text into sentences
sentences = nltk.sent_tokenize(transcript)

# Make empty lists
sentence_scores = []
sentiment_difference = []

# Get each sentence and sentence number, which is what enumerate does
for number, sentence in enumerate(sentences):
    # Use VADER to calculate sentiment
    scores = sentimentAnalyser.polarity_scores(sentence)
    # Make dictionary and append it to the previously empty list
    sentence_scores.append({'sentence': sentence, 'sentence_number': number+1, 'sentiment_score': scores['compound']})

df = pd.DataFrame(sentence_scores)
sentiment_difference = df['sentiment_score'] - df['sentiment_score'].shift(+1)
df = df.assign(sentiment_change = sentiment_difference)
df.to_csv('[sentiment score file pathname]', encoding='utf-8', index=False)
