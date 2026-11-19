# SMS Phishing & Smishing Detector (Nigerian Context), Version 2

Detects scam and phishing messages, including BVN, PIN, OTP, and fake-fee scams, using sentence embeddings. This is **Version 2**. Version 1 ([FILL IN link to your v1 repo]) failed on Nigerian-style scams, and this repo documents why and how v2 improved on it.

## Results
| Version | Method | Test | Result |
|---|---|---|---|
| v1 | Word counts (TF-IDF) + Logistic Regression | 60 Nigerian-context messages | **53.3%** (caught only 5 of 30 scams) |
| v1 + guardrails | Added keyword/behaviour features and a 0.35 threshold | same 60 messages | 81.7% *(development score: features and threshold were chosen while looking at these errors, so it is not an independent result)* |
| v2 | Sentence embeddings (all-mpnet-base-v2) + Logistic Regression | locked set of 80 messages, never tuned on | **91.2%** (35 of 40 scams caught, 2 false alarms) |
| v2, round 1 | same | 10 messages written by the author in his own words | 5 of 10 *(exposed a "selected = scam" shortcut)* |
| v2.1 (this repo's model) | v2 retrained with the author's messages and fixes | 30 messages from a separate source: [chatgpt] | 29 of 30 (96.7%) |

Each row uses different test data, so the numbers should not be averaged. All test sets are small.

## What went wrong in v1
Standard spam detectors score very high on public datasets, which are mostly UK/US text. My v1 model scored 98.6% on one of them, then **53.3%** on Nigerian-context scams. It missed 25 of 30, because those scams are worded differently: they ask the victim to hand over a BVN, PIN, or OTP instead of promising prizes or a premium-rate call. Counting words and phrases cannot recognise a scam that is simply reworded.
though after setting some guardrails **82.6%** was achieve which is not fair enough then i was prompt to start v2 which was train on Nigeria's data

## How v2 works
- Each message is turned into numbers that capture its **meaning** using a pretrained sentence model, so reworded scams land close together.
- A Logistic Regression classifier is trained on top, with Nigerian-context examples weighted 20x because there are far fewer of them.
- **Data:** about 4,000 general messages (a sample of the Mendeley balanced spam/smishing dataset), plus about 390 Nigerian-context scam and normal messages (BVN/PIN/OTP requests, fake alerts, scholarship and admission scams, pidgin, and many real-looking bank alerts and OTP messages labelled normal). These were written by me with AI assistance and are partly synthetic.
- Settings (weight, regularisation) were chosen with cross-validation. The 80-message test set was locked and run once.

## Honest findings and limitations
- **Shortcut learning:** Round 1 showed the model had learned "selected" = scam, because my scam examples all used that word and my normal examples didn't. Adding normal "you have been selected" notices and informal, typo-filled messages fixed most of it.
- **Real alerts vs fake alerts:** Real bank alerts and OTP messages were wrongly flagged until I added many of them as normal examples.
- **Text alone has a ceiling:** "You were selected, use this link to continue" can be real or a scam. In real life the sender and the link's domain decide.
- **Small tests:** 80, 30, and 10 messages are too few for precise accuracy figures, and the data was written by one author plus AI, so it shares a style.
- Not a substitute for caution. Never share a PIN, OTP, or BVN with anyone.

## Run it locally
1. `pip install -r requirements.txt`
2. `streamlit run app.py`

The first run downloads the embedding model (about 420 MB).

## Repo contents
- `app.py`: Streamlit web app
- `requirements.txt`: dependencies
- `phishing_detector_v2_1.joblib`: the trained classifier
- `phishing_detector_v2.ipynb`: the Colab notebook used for training and testing
- `base_reduced.csv`: sample of general messages used for training
- `nigerian_train.csv`: Nigerian-context training messages
- `train_first60.csv`: my first 60 Nigerian-context messages (training)
- `locked_test_80.csv`: the locked test set (80 messages), run once






## Data sources and credits
- Munoz, M. and Islam, M. (2025). *A Balanced Dataset for Spam and Smishing Detection using Large Language Models (LLMs)*. Mendeley Data, DOI 10.17632/vmg875v4xs.1, licensed CC BY 4.0.
- Pretrained model: `all-mpnet-base-v2` (Sentence-Transformers).
