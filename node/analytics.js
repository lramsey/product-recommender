var rec = require('./variables').rec;
var helpers = require('./helpers');
var Analytics = {};

Analytics.recommender = function(name, matrix){
  matrix = matrix || rec.recommendationMatrix;
  helpers._nameChecker(name);
  helpers._recVariableChecker();
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

Analytics.recommendByProduct = function(name, product){
  var matrix;
  if(product === undefined){
    matrix = rec.recommendationMatrix;
  }
  else{
    index = helpers._productClusterFinder(product);
    matrix = rec.subClustersHelpers[index][6];
  }
  return this.recommender(name, matrix);
};

Analytics.powerRecommendation = function(name){
  return this.recommender(name, rec.powerRecMatrix);
};

Analytics.pastCustomerRecommendations = function(name){
  helpers._nameChecker(name);
  helpers._recVariableChecker();
  return rec.pastRecommendations[name];
};

Analytics.getCustomerCluster = function(name){
  helpers._nameChecker(name);
  helpers._recVariableChecker();
  var index = rec.customerClusterHelpers[2][name];
  var cluster = rec.customerClusters[index].slice();
  return cluster;
};

Analytics.getCustomerClusterByProduct = function(name, product){
  helpers._nameChecker(name);
  helpers._productChecker(product);
  helpers._recVariableChecker();
  var subClustIndex = helpers._productClusterFinder(product);
  var map = rec.subClustersHelpers[index][2];
  var cluster = rec.subClusters[index];
  var related = cluster[map[name]].slice();
  return related;
};

Analytics.getProductCluster = function(product){
  var index = helpers._productClusterFinder(product);
  var cluster = rec.productClusters[index].slice();
  return cluster;
};

Analytics.relatedCustomers = function(name){
  var cluster = this.getCustomerCluster(name);
  cluster.splice(cluster.indexOf(name), 1);
  return cluster;
};

Analytics.relatedCustomersByProduct = function(name, product){
  var related = this.getCustomerClusterByProduct(name, product);
  related.splice(related.indexOf(name), 1);
  return related;
};

Analytics.relatedProducts = function(product){
  var cluster = this.getProductCluster(product);
  cluster.splice(cluster.indexOf(product), 1);
  return cluster;
};

Analytics.nearestNeighbors = function(name, num, overflow){
  return helpers._findNearestNeighbors(name, num, 'customers', overflow);
};

Analytics.nearestNeighborhoods = function(name, num){
  return helpers._findNearestNeighborhoods(name, num, 'customers');
};

Analytics.nearestProducts = function(name, num, overflow){
  return helpers._findNearestNeighbors(name, num, 'products', overflow);
};

Analytics.nearestProductNeighborhoods = function(name, num){
  return helpers._findNearestNeighborhoods(name, num, 'products');
};

module.exports = Analytics;
