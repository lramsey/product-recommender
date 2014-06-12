Product-Recommender NPM Module
=====================

This NPM module is a wrapping of my product recommendation engine from my python-recommender repo inside an npm module, so that it can easily be added to any node project.  This module exists on the npm registry under the name "product-recommender." This repo will have the up to date version of my python script, but if you want to see the earlier development of the script, please check out the python-recommender repo.  

The python script in the pyscript folder uses unguided machine learning to find trends within customer purchase data.  The algorithm expects three inputs: A list of customer names, a list of products under investigation, and a nested list that mentions how much of each product a customer has purchased.  Customers are divided into clusters of customers with similar purchase histories.  From these clusters, I derive recommendations by comparing the individual customer's buying patterns with the average buying patterns of the cluster.

Using the node.js command line interface through the built-in child_process module, the python script is run, streams its results to node.

**Set Up Process**

To utilize the product-recommender NPM module, the first step would be to make sure one has successfully installed node.js, npm, and a python version of >= 2.7 or >= 3.2.  To install these items, I would recommend you check out http://nodejs.org/download/ and https://www.python.org/download/.

In addition to these prerequisites, there are a couple python modules that you will need to install as well.  These modules are numpy and jsonpickle.  The install process for these modules is fairly simple, often just a few lines in the terminal.  For install instructions on numpy, please go to http://www.scipy.org/install.html.  For jsonpickle, please look at http://jsonpickle.github.io/#download-install.  Some more python modules used in this project are argparse, ast, math, and random, though these should be included in the Python Standard Library so there is likely no need to download these.

Once all of these dependencies are installed, adding the product-recommender module to your node project is as simple as navigating to your project directory in the terminal and typing 'npm install product-recommender', or 'npm install product-recommender --save' if you would like this module to be saved in your package.json.