// private object
var rec = {};
var GetSet = {};
var Variables = {'rec': rec, 'GetSet': GetSet};

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
GetSet.getRecVariable = function(key){
  if(rec[key] === undefined){
    throw new Error('not a valid recommendation variable');
  } else if(rec[key] === null){
    throw new Error('variable is null.  please run setRecVariables');
  } else{
    return rec[key];
  }
};

GetSet.getRecKeys = function(){
  return Object.keys(rec);
};

// use with caution
GetSet.loadRecVariable = function(key, value){
  if(rec[key] === undefined){
    throw new Error('not a valid recommendation variable');
  } else{
    rec[key] = value;
  }
};

// use with caution
GetSet.loadRecVariables = function(keys, values){
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

module.exports = Variables;
