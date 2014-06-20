# Product-Recommender NPM Module

## <a name='contents'/> Contents

[What is Product-Recommender?](#about)  
[Setup Process](#setup)  
[API](#use)  
[Recommendation Variables](#vars)  
[Recommendation Engine](#learn)  
[Analytics](#analysis)  

## <a name="about"/>  What is Product-Recommender?

Product-Recommender is an npm module that utlizes a python machine learning recommendation engine to give easy access to customer purchase recommendations.  Product-Recommender exists on the npm registry under the name "product-recommender." This repo will have the up to date version of my python recommendation engine, but if you wish to investigate the earlier development of the code, please check out my <a href='https://github.com/lramsey/python-recommender'>python-recommender</a> github repo.

The algorithm in the lib folder uses unsupervised machine learning to find trends within customer purchase data.  The algorithm expects three inputs: A list of customer names, a list of products under investigation, and a nested list that mentions how much of each product a customer has purchased.  The algorithm divides this product purchase quantity into two states: whether a customer has bought a product or has not bought a product.

Customers are divided into clusters based on similar purchase histories through a k-means algorithm.  From these clusters, the algorithm derives recommendations by comparing an individual customer's buying patterns with the average buying patterns of his or her cluster.  In addition, k-means is also used to group together products that tend to be bought together, and more focused customer clusters are constructed based on these product groups.  To learn more about the structure of my recommendation engine, please check out my blog post, <a href='http://lukeramsey.io/pythonrecommender'>Anatomy of a Recommendation</a>.

Using the node.js command line interface, the python recommendation engine can be launched as a child process, with the results streamed to node.  These results are divided into various variables based on the type of data they hold, and a user can gain access to all this raw analysis.  Or, a user may use helper methods within Product-Recommender to parse out desired information, such as which product to recommend to a consumer.

## <a name='setup'/> Setup Process

To utilize the Product-Recommender NPM module, the first step would be to make sure one has successfully installed node.js, npm, and a python version of >= 2.7 or >= 3.2.  To install these items, I would recommend you check out http://nodejs.org/download/ and https://www.python.org/download/.

In addition to these prerequisites, there are a couple python modules that you will need to install as well.  These modules are numpy and jsonpickle.  The install process for these modules is fairly simple, often just a few lines in the terminal.  For install instructions on numpy, please go to http://www.scipy.org/install.html.  For jsonpickle, please look at http://jsonpickle.github.io/#download-install.  Some more python modules used in this project are argparse, ast, math, and random, though these should be included in the Python Standard Library so there is likely no need to download these.

Once all of these dependencies are installed, adding the product-recommender module to your node project is as simple as navigating to your project directory in the terminal and typing 'npm install product-recommender'.

## <a name='use'/> API

Product-Recommender consists of three core parts, Recommendation Engine, Analytics, and Recommendation Variables.  In the Recommendation Engine section, the machine learning algorithm is run.  The results from this algorithm are then parsed and saved in the recommendation variables.  In the Analytics section, methods are provided that use the recommendation variables to produce desired outcomes. The Analytics methods do such things as finding groups of similar customer or producing a product recommendation for a customer.  In the Recommendation Variable section, I give you access to the Recommendation variables used by my Analytics methods, so you can use them however you see fit.

When using product-recommender though, the first step is to make sure you have required the module on the page you are using.As an example, for the rest of the readme project I will use the rec variable to represent my required module.
  
    var rec = require('product-recommender')

The three sections are listed below.  Pleas use these links to help in your navigation.

[Recommendation Engine](#learn)  
[Analytics](#analysis)  
[Recommendation Variables](#vars)  

## 1.<a name='learn'/> Recommendation Engine

This section consists of the setRecVariables method, which invokes the python recommendation engine.  When the algorithm has finished streaming its results to node, the setRecVariables method then parses these results and assigns values to each of the recommendation variables.  Whenever one wants a fresh reading of the recommendation engine's analysis, one simply needs to run setRecVariables method again and the recommendation variables will be set to the values of the latest analysis.

The setRecVariables method takes four parameters: 

    rec.setRecVariables(history, callback, names, products)

**history**

The history argument contains a 2-D array or matrix.  Each entry in the outer array contains the purchase history of an individual customer.  The length of the outer array is the same length as the names array below, so each customer in the data set is represented in the history parameter.  The length of each inner array is the length of the products array below.  Each inner array contains information on which product from the products list each customer has purchased.  The order of products in the inner array should match the order in the products array, so each column of the 2-D array refers to a particular product.

      var history = [ [1,0,0], [1,1,1], [0,1,1] ]
    
**callback**

The callback parameter consists of a custom callback function that will run after my product recommendation engine has finished streaming its results to node.js.  The algorithm runs asynchronously, so properly putting your continuing product-recommender logic inside a callback function is essential to using product-recommender.

      var callback = function(){ results = rec.getRecVariables('results')) }

**names**
      
The names argument consists of an array of customer names/unique identifiers.  Each element in this array should be a unique string.

If a names argument is not used, the parameter will default to a number n which is the length of the outer array in the history paremeter nested array.  A names array of length n will be created and filled with random unique name strings for each index in the array.

      var names = [ 'Steve', 'Henry', 'Thea', 'Patrick' ]

**products**
      
The products argument consists of an array of product names/unique identifiers.  Like the names parameter, each element in this array should be a unique string.

If a products argument is not used, the parameter will default to a number n which is the same length of any of the inner arrays in the history parameter nested array.  A products array of length n will be created and filled with random unique product strings for each index in the array.

      var products = [ 'shoes', 'socks', 'shirts', 'shorts' ]

[API](#use)

## 2.<a name='analysis'/> Analytics

This grouping consists of methods that are designed to analyze the data held in the recommendation variables to produce a desired result.  These methods accomplish such goals as determining which cluster is most relevant to a customer's purchase of a particular product or producing a product recommendation for a customer based on recent buying patterns. Now I will describe the analytics functions.
    
**recommender(customer, recMatrix)**

This method accepts inputs of a customer string from the customer array and the optional input of a recommendation matrix.  The method considers the input customer's row from the recommendation matrix and pops off the product that my algorithm has determined is the strongest recommendation in that group.  The recommended product is returned.

The recommendation matrix parameter allows the more custom recommendation matrices built around buying trends in related product groups to be used instead of the default matrix.  If a user buys a pair of shoes, he may have a certain taste in products similar to shoes that is different than his taste in other areas.  By placing the recommendation matrix concerned with the shoe products in the recommender method, the recommendation can be fine tuned based on the reality that the user recently bought shoes.  With this custom matrix parameter, one can choose which product group of interest one wants the recommendation tailored towards.

    rec.recommender('Steve', matrix)

**recommendByProduct(customer, product)**

This method takes a customer string and a product string as parameters.  The method then determines which product group the product belongs to, and accesses the proper recommendation matrix based on that product group.  This custom recommendation matrix is then used to return a product more focused on the customers buying patterns in relation the input product.

    rec.recommendByProduct('Steve', 'shoes')

**relatedCustomers(customer)**

This method accepts a customer string as a parameter and returns an array of customers with similar purchase histories based on clustering.  This result refers to the global cluster group.  To investigate more focused groups based on certain product patterns, please use the the relatedCustomersByProduct method.

    rec.relatedCustomers('Steve')

**relatedCustomersByProduct(customer, product)**

This method takes a customer string and product string as a parameter. The method returns that customer's cluster based on the input product.  The members of this cluster will have similar buying patterns with the input customer in terms of products similar to the product parameter.

    rec.relatedCustomersByProduct('Steve', 'shoes')

**relatedProducts(product)**

This method takes a product string as a parameter.  The method returns an array of products my algorithm has judged to be similar based on the aggregate purchase history of my customers.

    rec.relatedProducts('shoes')

[API](#use)

## 3.  <a name='vars'/> Recommendation Variables

The recommendation variables hold the fine-grained results from my product recommendation algorithm.  These results can be accessed overall by the results variable, or can be broken into various categories.  To access a recommendation variable, one would call the getRecVariable method, passing the desired variable name in as a key.

    rec.getRecVariable(key);

To receive an array containing all of the recommendation keys, one can call the getRecKeys() method. 

     rec.getRecKeys();

Initially the recommendation variables will be set to null, until a call is made to launch the python recommendation engine.  Now, I will describe the recommendation variables.

**results**

An array containing all of the below recommendation variables except for rawResults.

**rawResults**

An array containing the raw results sent from my product recommendation algorithm.
  
**customers**
    
An array containing the name string of every customer.  The order of customers in this array matches the customer order in the succeeding matrices.
  
**products**

An array containing the name string of every product.  The order of products in this array matches the product order in the history matrix.

**purchaseHistory**
   
A nested array containing the raw purchase history nested array passed in as a parameter to the setRecVariables method.  Each index in the outer array refers to a customer, and each index in the inner array refers to how much of a particular product a customer bought.

**hasPurchased**
   
A nested array containing a normalized version of the history array passed in as a parameter to the setRecVariables method.  For every integer greater than 1 in the nested array, that value will be set to one.  This matrix serves as a boolean indicator on whether a customer has bought a product or not.  This matrix is used in my product recommendaton analysis, whereas the history matrix is not.

**customersMap**
  
An object that contains each customer's string name as keys, with corresponding values referring to which index that string is stored in the customers array and various matrices.

**productsMap**
  
An object that contains each product's string name as keys, with corresponding values referring to which index that string is stored in the products array and history matrix.

**productClusters**
  
 A nested array structure.  Each array refers to a grouping of products that the product-recommendation algorithm has determined are similar based on aggregate customer buying patterns.

**productClustersMap**

An object that takes a product as a key.  The corresponding value would be the index one can use in the productClusters array to find the group of products most similar to the input product.

**customerClusters**
  
 A nested array structure.  Each array refers to a grouping of customers based on similar purchase trends based on the total product set.

**recommendationMatrix**
  
A nested array that organizes customer recommendations based on the groupings listed in the customerClusters variable.  These recommendations are ordered, so the last product in each inner array is the product my algorithm has determined is the best product to recommend based on the customerClusters.  Also, these products contain metadata

**customerClusterHelpers**

An array of seven useful tools in relation to the customerClusters.  I will describe each element by its index in the array.
    
Index 0 contains the customerClusters.

Index 1 contains an array of centroid values for each cluster, where centroid 
refers to the average purchase trends of every customer within a group. 

Index 2 contains a clusterMap object that contains a key of customer names and a corresponding number referring to which cluster that customer is in.  That number refers to the index of a particular cluster in the customerClusters array.
    
Index 3 contains an indexMap object that contains a key of a customer name and a corresponding number that refers to what index inside that customer's cluster the customer name currently lies.
    
Index 4 contains an array of silhouettes.  A silhouette is a number between 0 and 1 that represents how much closer members of a cluster are with their own cluster center in comparison to the cluster center of the next closest cluster. The closer the silhouette is to 1, the stronger the clusters.  Each silhouette score refers to a grouping in the customerClusters array, and the order is the same as the order in that array.

Index 5 contains an average of all the cluster silhouettes in index 4.  This serves as a rough indicator of the strength of all the clustering in customerClusters.
      
Index 6 contains the recommendationMatrix that is built up based on the customerClusters.  This presents ordered product recommendations for each customer, with the last element of each customer array referring to the product my algorithm most highly recommends based on the customerCluster.
  
**subClusters**

An array containing all the more focused customer clustering that is determined by the product groupings found in productClusters.  Customers in these subClusters are grouped with other customers based on their similar buying patterns in relation to these smaller product groups.

**subClustersHelpers**

An array containing a series of 7 element arrays similar to the customerClusterHelpers, but with various subClusters replacing the customerClusters.  Each element in the subClusters array will have its own subClusterHelper.

**powerClusters**

An array of that contains elements from the subClusters, but has removed subClusters with a relatively low average silhouette score.

**powerClustersHelpers**

Similar to subClusterHelpers, but containing elements from the powerClusters array.

**powerRecMatrix**

A recommendation matrix built by compiling together the results from the powerClusters and the global customerClusters.  The strongest elements from each type of cluster are weighted by silhouette scores and ordered by recommendation strength.

**pastRecommendations**

An object that contains a key for each customer in the dataset.  Each customer key has a corresponding value that is an object.  The inner object contains keys with a true for each product which has been recommended to the designated customer.


[API](#use)  
[Contents](#contents)  