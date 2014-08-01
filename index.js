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
rec.customerMatrix         = null;
rec.productMatrix          = null;
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

// use with caution
Recommender.loadRecVariable = function(key, value){
  if(rec[key] === undefined){
    throw new Error('not a valid recommendation variable');
  } else{
    rec[key] = value;
  }
};

// use with caution
Recommender.loadRecVariables = function(keys, values){
  if(keys.length > values.length){
    throw new Error('Each key must have a value');
  } else if (keys.length < values.length){
    throw new Error('Each value must have a key');
  } else{
    keys.forEach(function(key, i){
      this.loadRecVariable(key, values[i]);
    });
  }
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

Recommender.powerRecommendation = function(name){
  return this.recommender(name, rec.powerRecMatrix);
};

Recommender.pastCustomerRecommendations = function(name){
  _nameChecker(name);
  _recVariableChecker();
  return rec.pastRecommendations[name];
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

Recommender.nearestNeighbors = function(name, num, overflow){
  return _findNearestNeighbors(name, num, 'customers', overflow);
};

Recommender.nearestNeighborhoods = function(name, num){
  return _findNearestNeighborhoods(name, num, 'customers');
};

Recommender.nearestProducts = function(name, num, overflow){
  return _findNearestNeighbors(name, num, 'products', overflow);
};

Recommender.nearestProductNeighborhoods = function(name, num){
  return _findNearestNeighborhoods(name, num, 'products');
};

_findNearestNeighborhoods = function(name, num, type){
  var map;
  var matrix;
  var list;
  if(type === 'customers'){
    map = rec.customersMap;
    matrix = rec.customerMatrix;
    list = rec.customers;
    _nameChecker(name);
  } else if(type === 'products'){
    map = rec.productsMap;
    matrix = rec.productMatrix;
    list = rec.products;
    _productChecker(name);
  } else{
    throw new Error('Invalid type.  Find neighbors for customers or products.');
  }
  _recVariableChecker();
  num = num || 1;
  if(typeof(num) !== 'number' || num%1 !== 0){
    throw new Error('second parameter should be an integer');
  }
  var index = map[name];
  var dists = matrix[index];
  var similarity = [];
  var results = [];
  var ind;
  var obj;

  dists.forEach(function(dist, i){
    if(index !== i){
      if(similarity.length < num || dist < similarity[similarity.length-1]){
        ind = _binarySearch(dist, similarity);
        if(similarity[ind] === dist){
          results[ind][dist].push(list[i]);
        } else{
          if(dist < similarity[similarity.length-1] && similarity.length >= num){
            similarity.pop();
            results.pop();
          }
          similarity.splice(ind, 0, dist);
          obj  = {};
          obj[dist] = [list[i]];
          results.splice(ind, 0, obj);
        }
      }
      else if (dist === similarity[similarity.length-1]){
        results[similarity.length-1][dist].push(list[i]);
      }
    }
  });

  return results;
};


var _findNearestNeighbors = function(name, num, type, overflow){
  var results = [];
  var i;
  var neighborhood;
  var neighbor;
  num = num || 1;
  if(overflow === undefined){
    overflow = true;
  }
  
  var neighbors = this._findNearestNeighborhoods(name, num, type);
  for(i = 0; i < num; i++){
    if(results.length < num){
      for(var j in neighbors[i]){
          neighborhood = neighbors[i][j];
        for(var k = 0; k < neighborhood.length; k++){
          neighbor = neighborhood[k];
          results.push(neighbor);
        }
      }
    } else {
      break;
    }
  }

  if(!overflow){
    for(i = num; i < results.length; i++){
      results.pop();
    }
  }
  return results;
};
  
var _nameChecker = function(name){
  if(name === undefined || typeof(rec.customersMap[name]) !== 'number'){
    throw new Error('invalid name. name does not exist in the data set.');
  }
};

var _productChecker = function(product){
  if(product === undefined || typeof(rec.productsMap[product]) !== 'number'){
    throw new Error('invalid product. product does not exist in the data set.');
  }
};

var _recVariableChecker = function(){
  if (rec.results === 'null'){
    throw new Error('recommendation variables are null. please run setRecVariables');
  }
};

var _productClusterFinder = function(product){
  _recVariableChecker();
  _productChecker(product);
  var index = rec.productClustersMap[product];
  return index;
};

var _binarySearch = function(item, arr, low, high){
  low = low || 0;
  high = high || arr.length;
  var median = Math.floor((low+high)/2);
  if(low === high){
    return high;
  }
  else if(item < arr[median]){
    if(low === median){
      return low;
    }
    return _binarySearch(item, arr, low, median);
  }
  else if(item > arr[median]){
    if(low === high-1){
      return _binarySearch(item, arr, low+1, high);
    }
    return _binarySearch(item, arr, median, high);
  }
  else{
    return median;
  }
};


/* ------------------------------------------------------------------------------------*/

module.exports = Recommender;
