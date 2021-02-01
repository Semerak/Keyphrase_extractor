# Keyphrase extractor

#### install dependencies

```pip install nltk```

```pip install wikipedia```

#### download additional files for light model (optionally)

Download a zip file of the GloVe embedding vectors (http://nlp.stanford.edu/data/glove.6B.zip). Unpack it and move file glove.6B.300d.txt to directory lib/GloVe. 

### How the keyprhase extractor works
1. The input text is pre-processed: lowercase, deleting all not-word symbols.
2. Nltk tokenizer split text to list of words. Stop words are deleted.
3. Count n-grams (n=1,2) and sort by frequency.
4. (optional) Include Light model.
5. Return the list of keyprases, which has a length < ```max_keys``` and the lowest-scored keyprase has a score > max_scored * ```alpha```. Parameters max_keys and alpha can be modified form front.
  
  ```max_keys``` - Maximum number of keywords
  ```alpha``` - Coefficient for threshold value
  
### Light model 
Represent words as fireflies (or stars). Every word light up other nearest words. The GloVe's embedding vectors are used to define coordinates of the words. The frequency of the word in given text represents its size and brightness. Then we calculate the total light of each word as sum of its own light and the light given by other words to this word. This sum is a new ranking for keyprases. Such model takes into account similar by meaning words.