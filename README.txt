Libraries used:
    1.Pandas
    2.re
    3.math

Executables:
    Original training and testing
    1. training.py: Model without any extra cleaning => model-2018.txt
    2. testing.py: Test based on the model-2018. => baseline-result.txt

    Experiment 1: Stop-word Filtering
    3. stopword_train.py: Model with stopwords cleaning. => stopword-model.txt
    4. stopword_test.py: Test based on the stopword-model. => stopword-result.txt

    Experiment 2: Word Length Filtering
    5. wordLength_train.py: Model with word length cleaning. => wordLength-model.txt
    6. wordLength_test.py: Test based on the wordLength-model. => wordLength-result.txt

    Experiment 3: Infrequent Word Filtering
    frequency_train.py :
        7. Gradually remove the words with frequency <=1 , <=5, <=10, <=15, <=20. Then calculate the performance corresponding to these cleanings.
        8. Gradually remove the words with frequency >5% , >10%, >15%, > 20%, >25%. Then calculate the performance corresponding to these cleanings.
        conclusion:
            The more the low-frequent words are removed , the higher the performance will be.
            But the more the high-frequent words are removed, the lower the performance will be.
