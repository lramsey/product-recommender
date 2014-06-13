# Product-Recommender NPM Module

## Contents
[What is Product-Recommender?](#about)
[Setup Process](#setup)
[API](#use)

## <a name="about"/>  What is Product-Recommender

Product-Recommender is an npm module that utlizes a python machine learning recommendation engine to give easy access to customer purchase recommendations.  Product-Recommender exists on the npm registry under the name "product-recommender." This repo will have the up to date version of my python recommendation engine, but if you wish to see the earlier development of the script, please check out my <a src='https://github.com/lramsey/python-recommender'>python-recommender</a> github repo.

The python script in the pyscript folder uses unguided machine learning to find trends within customer purchase data.  The algorithm expects three inputs: A list of customer names, a list of products under investigation, and a nested list that mentions how much of each product a customer has purchased.  Customers are divided into clusters based on similar purchase histories through a k-means algorithm.  From these clusters, the algorithm derives recommendations by comparing an individual customer's buying patterns with the average buying patterns of his or her cluster.  To learn more about the structure of my recommendation engine, please check out my blog post, <a src ='http://lukeramsey.io/pythonrecommender'>Anatomy of a Recommendation</a>.

Using the node.js command line interface, the python recommendation engine can be invoked, with the results streamed to node.
These results are divided into various variables based on the type of data they hold, and a user can gain access to all this raw analysis.  Or, a user may use helper methods within Product-Recommender to parse out desired information, such as which product to recommend to a consumer.

## <a name='setup'/> Setup Process

To utilize the Product-Recommender NPM module, the first step would be to make sure one has successfully installed node.js, npm, and a python version of >= 2.7 or >= 3.2.  To install these items, I would recommend you check out http://nodejs.org/download/ and https://www.python.org/download/.

In addition to these prerequisites, there are a couple python modules that you will need to install as well.  These modules are numpy and jsonpickle.  The install process for these modules is fairly simple, often just a few lines in the terminal.  For install instructions on numpy, please go to http://www.scipy.org/install.html.  For jsonpickle, please look at http://jsonpickle.github.io/#download-install.  Some more python modules used in this project are argparse, ast, math, and random, though these should be included in the Python Standard Library so there is likely no need to download these.

Once all of these dependencies are installed, adding the product-recommender module to your node project is as simple as navigating to your project directory in the terminal and typing 'npm install product-recommender'.

## <a name='use'/> API

Product-Recommender consists of three core parts:

1)  Reccommendation Variables:

The recommendation variables hold the raw results from my product recommendation algorithm.  These results can be accessed overall by the results variable, or can be broken into various categories.  To access a reccommendation variable, one would call the getRecVariables() method, passing the desired variable name in as a key.  To see the complete list of recommendation variables, one can call the getRecKeys() method. Initially the reccommendation variables will be set to null, until a call is made to launch the python recommendation engine.  Now, I will describe the recommendation variables.



1)  Set Reccomendation Variables:

This section consists of the setRecVariables method, which invokes the python recommendation engine.  When the algorithm has finished streaming its results to node, the setRecVariables method then parses these results and assigns values to each of the recommendation variables.  Whenever one wants a fresh reading of the recommendation engine's analysis, one simply needs to run setRecVariables method again and the reccommendation variables will be set to the values of the latest analysis.

The setRecVariables method requires three arguments:

    I)   names
      
      The names argument consists of an array of customer names/unique identifiers.  Each element in this array should be a unique string.

      Optionally, one may place a number n in to the names parameter instead of an array, and the product recommendation engine will generate an array of length n.  This array will be filled with random unique names for each index in the array.

    II)  products
      
      The products argument consists of an array of product names/unique identifiers.  Like the names parameter, each element in this array should be a unique string.

      Optionally, the products parameter can also be replaced by a number n to create a unique product array of length n.

    III) history

      The history argument contains 2-D array or matrix.  Each entry in the outer array contains the purchase history of an individual customer.  The length of the outer array is the same length as the names array, so each customer in the data set is represented in the history parameter.  The length of each inner array is the length of the products array.  Each inner array contains information on which product from the products list each customer has purchased.  The order of products in the inner array will match the order in the products array, so each row of the 2-D array refers to a particular product.

      Optionally, if one wishes to create mock data, one may enter the history argument as 'False', and the algorithm will generate a random matrix based on the length of the names array and the products array.

3)  Analysis & Product Recommendation:

This grouping consists of methods that are designed to analyze the data held in the recommendation variables and produce a desired outcome.  These methods accomplish such goals as returning a user's fellow group members based on an individual product, or producing a product recommendation for a customer based on recent buying patterns.  Now I will describe the analysis functions.
    
    I) recommender():
      This method accepts inputs of a customer string from the customer array and the optional input of a recommendation matrix.  The method considers the input customer's row from the recommendation matrix and pops off the product that my algorithm has determined is the strongest recommendation in that group.  The recommended product is returned.

      The recommendation matrix parameter allows the more custom recommendation matrix built around individual products to be inputIf no recommendation matrix is input, the function will default to the recommendation variable named recommendationMatrix.