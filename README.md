# word2vec-recommender

[Talk Submission at Pycon India 2016](https://in.pycon.org/cfp/2016/proposals/creating-a-recommendation-engine-based-on-contextual-word-embeddings~aOZGe/)

## Index
- [What it is ??](#what-it-is?) 
- [How it is done?](#how-it-is-done?)
- [Technologies used](#technologies-used)
- [Installation](#installation)
- [What is there inside the box :package: ?](#What-is-there-inside-the-box?)
- [Contributors](#contributors)
- [Issues](#issues)

## What it is?
How can we create a recommendation engine that is based both on user browsing history and product reviews? Can I create recommendations purely based on the 'intent' and 'context' of the search?

This talk will showcase how a recommendation engine can be built with user browser history and user-generated reviews using a state of the art technique - word2vec. We will create something that not only matches the existing recommender systems deployed by websites, but goes one step ahead - incorporating context to generate valid and innovative recommendations. The beauty of such a framework is that not only does it support online learning, but is also sensitive to minor changes in user tone and behavior.

## How it is done?

The trick/secret sauce is - How do we account for the 'context' and build it in our systems? The talk will answer these questions and showcase effectiveness of such a recommender system.

## Technologies used

* Google's Word2vec
* Gensim
* Numpy
* Flask, Redis.

## Installation

* [Lets do it !!](https://github.com/manasRK/word2vec-recommender/blob/master/Python%20Cloud%20Setup.md) 

## What is there inside the box?

| File                  | Function                  | 
|:---------------------:|:-------------------------:| 
| semsim_train.py       | Main file to train models | 
| preProcessing.py      | Methods to preprocess and clean data before feeding for training |
| loadReviewModel.py    | For loading review model  |
| loadRedis.py          | For loading redis model   |   
| loadMetaModel.py      | For loading meta model    |  

## contributors

|    Author        |              Working As             | contact @|
| -------------    |:-----------------------------------:| -----:  |
| Manas Ranjan kar | Practice Lead @ Juxt Smart Mandate  |[@github](https://github.com/manasRK) |
| Akhil Gupta      | Intern @ Amazon              |   [@github](https://github.com/codeorbit) |
| Vinay Kumar      | MS @ IIT-KGP                        |    [@github](https://github.com/vinay2k2)   |

## Issues
You can [Manas Ranjan kar](https://twitter.com/manasrnkar) [Akhil Gupta](https://twitter.com/decoding_life) if you can't get it to work. In fact, you should tweet us anyway.


