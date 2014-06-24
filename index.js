// private object
var rec = {};
// object to export
var Recommender = {};

/* ------------------------------------------------------------------------------------*/
/* Recommendation Variables
/*
/* ------------------------------------------------------------------------------------*/

rec.results                = null;
rec.rawResults             = null;
rec.customers              = null;
rec.products               = null;
rec.purchaseHistory        = null;
rec.hasPurchased           = null;
rec.customersMap           = null;
rec.productsMap            = null;
rec.productClusters        = null;
rec.productClustersMap     = null;
rec.customerClusterHelpers = null;
rec.customerClusters       = null;
rec.recommendationMatrix   = null;
rec.subClustersHelpers     = null;
rec.subClusters            = null;
rec.powerClustersHelpers   = null;
rec.powerClusters          = null;
rec.powerRecMatrix         = null;
rec.pastRecommendations    = null;

// can only directly access these keys through below methods
Recommender.getRecVariable = function(key){
  if(rec[key] === undefined){
    throw new Error('not a valid recommendation variable');
  } else if(rec[key] === null){
    throw new Error('variable is null.  please run setRecVariables');
  } else{
    return rec[key];
  }
};

Recommender.getRecKeys = function(){
  return Object.keys(rec);
};

/* ------------------------------------------------------------------------------------*/
/* Recommendation Engine
/*
/* ------------------------------------------------------------------------------------*/

Recommender.setRecVariables = function(matrix, cb, names, prods){
  names = names || matrix.length;
  prods = prods || matrix[0].length;
  cb = cb || function(){};
  var i;

  mat = JSON.stringify(matrix);
  names = JSON.stringify(names);
  prods = JSON.stringify(prods);

  var python = require('child_process').spawn(
    'python',
    [__dirname + '/lib/exec.py', names, prods, mat]);
  output = '';
  python.stdout.on('data', function(data){
    output += data;
  });
  python.stdout.on('close', function(){
    _buildRecVariables(output, matrix);
    args = Array.prototype.slice.call(arguments,4);
    cb.apply(this,args);
  });
};

_buildRecVariables = function(output, matrix){
  var results = JSON.parse(output);

  rec.rawResults             = results;
  rec.customers              = results[0];
  rec.products               = results[4];
  rec.purchaseHistory        = matrix;
  rec.hasPurchased           = results[9];
  rec.customersMap           = results[1];
  rec.productsMap            = results[3];
  rec.productClusters        = results[2];
  rec.productClustersMap     = results[10];
  rec.customerClusterHelpers = results[6];
  rec.customerClusters       = rec.customerClusterHelpers[0];
  rec.recommendationMatrix   = rec.customerClusterHelpers[6];
  
  rec.subClustersHelpers     = [];
  var productClusterLocator  = results[11];
  for(i = 0; i < productClusterLocator.length; i++){
    var locator = productClusterLocator[i];
    if(locator[0] === 'sub'){
      rec.subClustersHelpers.push(results[7][locator[1]]);
    } else if(locator[0] === 'power'){
      rec.subClustersHelpers.push(results[8][locator[1]]);
    }
  }
  
  rec.subClusters            = [];
  for(i = 0; i < rec.subClustersHelpers.length; i++){
    rec.subClusters.push(rec.subClustersHelpers[i][0]);
  }
  rec.powerClustersHelpers   = results[8];
  rec.powerClusters          = [];
  for(i = 0; i < rec.powerClustersHelpers.length; i++){
    rec.powerClusters.push(rec.powerClustersHelpers[i][0]);
  }
  rec.powerRecMatrix         = results[5];
  rec.pastRecommendations    = {};
  for(i=0; i< rec.customers.length; i++){
    rec.pastRecommendations[rec.customers[i]] = {};
  }
  
  rec.results                = [rec.customers, rec.products, rec.purchaseHistory, rec.hasPurchased, rec.customersMap,
                                rec.productsMap, rec.productClusters, rec.productClustersMap, rec.customerClusterHelpers,
                                rec.customerClusters, rec.recommendationMatrix, rec.subClustersHelpers, rec.subClusters,
                                rec.powerClustersHelpers, rec.powerClusters, rec.powerRecMatrix, rec.pastRecommendations];
};

/* ------------------------------------------------------------------------------------*/
/* Analytics
/*
/* ------------------------------------------------------------------------------------*/


Recommender.recommender = function(name, matrix){
  matrix = matrix || rec.recommendationMatrix;
  _nameChecker(name);
  _recVariableChecker();
  var recommendation = matrix[rec.customersMap[name]].pop();
  var attraction = Object.keys(recommendation)[0];
  var product = recommendation[attraction];
  if(rec.pastRecommendations[name][product] === true){
    return this.recommender(name,matrix);
  } else{
    rec.pastRecommendations[name][product] = true;
  }
  return product;
};

Recommender.recommendByProduct = function(name, product){
  var matrix;
  if(product === undefined){
    matrix = rec.recommendationMatrix;
  }
  else{
    index = _productClusterFinder(product);
    matrix = rec.subClustersHelpers[index][6];
  }
  return this.recommender(name, matrix);
};

Recommender.relatedCustomers = function(name){
  _nameChecker(name);
  _recVariableChecker();
  var index = rec.customerClusterHelpers[2][name];
  var cluster = rec.customerClusters[index];
  return cluster;
};

Recommender.relatedCustomersByProduct = function(name, product){
  _nameChecker(name);
  _productChecker(product);
  _recVariableChecker();
  var subClustIndex = _productClusterFinder(product);
  var map = rec.subClustersHelpers[index][2];
  var cluster = rec.subClusters[index];
  var related =cluster[map[name]];
  return related;
};

Recommender.relatedProducts = function(product){
  var index = _productClusterFinder(product);
  var cluster = rec.productClusters[index];
  return cluster;
};

_nameChecker = function(name){
  if(name === undefined || typeof(rec.customersMap[name]) !== 'number'){
    throw new Error('invalid name. name does not exist in the data set.');
  }
};

_productChecker = function(product){
  if(product === undefined || typeof(rec.productsMap[product]) !== 'number'){
    throw new Error('invalid product. product does not exist in the data set.');
  }
};

_recVariableChecker = function(){
  if (rec.results === 'null'){
    throw new Error('recommendation variables are null. please run setRecVariables');
  }
};

_productClusterFinder = function(product){
  _recVariableChecker();
  _productChecker(product);
  var index = rec.productClustersMap[product];
  return index;
};

/* ------------------------------------------------------------------------------------*/

module.exports = Recommender;
