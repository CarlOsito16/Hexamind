# Summarization and Keyword Extraction
---


Please find the demo on hugging face >> [*here*](https://huggingface.co/spaces/Carlosito16/HXM-summarization)

## 🏁 Goal
Given the customer reviews from public website such as Trustadvisor, this demo aims to perform two NLP tasks for the French Language:
- **Text Summarization**: the input is the given text, and the default summarization pre-trained bert model of `'mrm8488/camembert2camembert_shared-finetuned-french-summarization'` is running to generate the summary
- **Key Word Extraction**: To achieve the key word extraction, below is the pipline

<img width="700" alt="Screen Shot 2566-02-08 at 12 37 18" src="https://user-images.githubusercontent.com/78911624/217519988-d3d8a0f0-e381-494e-bd9a-f1a2e5f73597.png">


The defaut `top_n` hyperparameter for `NOUN` token is 3. This should suggest the top most relevant words that could be later used for clustering when having larger dataset of reviews.

As for the `PROPN` or `proper noun` tokens, not every review has this word, thus the model can also return blank. The purpose of this proper noun extraction is to give a more fine-grained insights into plausibly product brands, branch names, city etc.

---
# File Description
- Hexamind_resume.ipynb: the first and original file developed on colab, it contains all the workflow from end to end
- GenerateSummary.ipynb: this file is to only call the functions developed prior to generate summary and keywords based on the manually dataset at 20230220 
