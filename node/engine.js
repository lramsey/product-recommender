var rec = require('./variables').rec;
var Engine = {};

Engine.setRecVariables = function(matrix, cb, names, prods){
  names = names || matrix.length;
  prods = prods || matrix[0].length;
  cb = cb || function(){};
  var i;

  mat = JSON.stringify(matrix);
  names = JSON.stringify(names);
  prods = JSON.stringify(prods);

  var python = require('child_process').spawn(
    'python',
    [__dirname + '/../lib/exec.py', names, prods, mat]);
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

var _buildRecVariables = function(output, matrix){
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
  rec.customerMatrix         = results[12];
  rec.productMatrix          = results[13];
  rec.customerClusterHelpers = results[6];
  rec.customerClusters       = rec.customerClusterHelpers[0];
  rec.recommendationMatrix   = rec.customerClusterHelpers[6];
  
  rec.subClustersHelpers     = [];
  var productClusterLocator  = results[11];

  productClusterLocator.forEach(function(locator){
    if(locator[0] === 'sub'){
      rec.subClustersHelpers.push(results[7][locator[1]]);
    } else{
      rec.subClustersHelpers.push(results[8][locator[1]]);
    }
  });
  
  rec.subClusters            = [];
  rec.subClustersHelpers.forEach(function(helper){
    rec.subClusters.push(helper[0]);
  });

  rec.powerClustersHelpers   = results[8];
  rec.powerClusters          = [];

  rec.powerClustersHelpers.forEach(function(helper){
    rec.powerClusters.push(helper[0]);
  });
  rec.powerRecMatrix         = results[5];
  
  rec.pastRecommendations    = {};
  rec.customers.forEach(function(customer){
    rec.pastRecommendations[customer] = {};
  });

  rec.results                = [rec.customers, rec.products, rec.purchaseHistory, rec.hasPurchased, rec.customersMap,
                                rec.productsMap, rec.productClusters, rec.productClustersMap, rec.customerMatrix, rec.productMatrix,
                                rec.customerClusterHelpers,rec.customerClusters, rec.recommendationMatrix, rec.subClustersHelpers,
                                rec.subClusters, rec.powerClustersHelpers, rec.powerClusters, rec.powerRecMatrix, rec.pastRecommendations];
};

module.exports = Engine;
