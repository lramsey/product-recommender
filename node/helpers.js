var rec = require('./variables').rec;
var helpers = {};

helpers._findNearestNeighborhoods = function(name, num, type){
  var map;
  var matrix;
  var list;
  if(type === 'customers'){
    map = rec.customersMap;
    matrix = rec.customerMatrix;
    list = rec.customers;
    this._nameChecker(name);
  } else if(type === 'products'){
    map = rec.productsMap;
    matrix = rec.productMatrix;
    list = rec.products;
    this._productChecker(name);
  } else{
    throw new Error('Invalid type.  Find neighbors for customers or products.');
  }
  this._recVariableChecker();
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
        ind = this._binarySearch(dist, similarity);
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
  }.bind(this));

  return results;
};


helpers._findNearestNeighbors = function(name, num, type, overflow){
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
  
helpers._nameChecker = function(name){
  if(name === undefined || typeof(rec.customersMap[name]) !== 'number'){
    throw new Error('invalid name. name does not exist in the data set.');
  }
};

helpers._productChecker = function(product){
  if(product === undefined || typeof(rec.productsMap[product]) !== 'number'){
    throw new Error('invalid product. product does not exist in the data set.');
  }
};

helpers._recVariableChecker = function(){
  if (rec.results === 'null'){
    throw new Error('recommendation variables are null. please run setRecVariables');
  }
};

helpers._productClusterFinder = function(product){
  this._recVariableChecker();
  this._productChecker(product);
  var index = rec.productClustersMap[product];
  return index;
};

helpers._binarySearch = function(item, arr, low, high){
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
    return this._binarySearch(item, arr, low, median);
  }
  else if(item > arr[median]){
    if(low === high-1){
      return this._binarySearch(item, arr, low+1, high);
    }
    return this._binarySearch(item, arr, median, high);
  }
  else{
    return median;
  }
};

helpers._extend = function(obj1){
  args = Array.prototype.slice.call(arguments, 1);
  args.forEach(function(obj){
    for(var key in obj){
      obj1[key] = obj[key];
    }
  });
};

module.exports = helpers;
