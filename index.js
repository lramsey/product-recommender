var rec = {};

rec.rawResults             = null;
rec.customers              = null;
rec.products               = null;
rec.history                = null;
rec.hasPurchased           = null;
rec.customersMap           = null;
rec.productsMap            = null;
rec.productClusters        = null;
rec.customerClusterHelpers = null;
rec.customerClusters       = null;
rec.recommendationMatrix   = null;
rec.subClusterHelpers      = null;
rec.subClusters            = null;
rec.powerClustersHelpers   = null;
rec.powerClusters          = null;
rec.powerRecMatrix         = null;
rec.results                = null;

module.exports = Recommender = {
  setRecVariables: function(matrix, cb, names, prods){
    names = names || matrix.length;
    prods = prods || matrix[0].length;
    cb = cb || function(){};
    var i;

    mat = JSON.stringify(matrix);
    names = JSON.stringify(names);
    prods = JSON.stringify(prods);

    var python = require('child_process').spawn(
      'python',
      [__dirname + '/pyscript/exec.py', names, prods, mat]);
    output = '';
    python.stdout.on('data', function(data){
      output += data;
    });
    python.stdout.on('close', function(){
      results = JSON.parse(output);
      rec.rawResults             = results;
      rec.customers              = results[0];
      rec.products               = results[4];
      rec.history                = matrix;
      rec.hasPurchased           = results[9];
      rec.customersMap           = results[1];
      rec.productsMap            = results[3];
      rec.productClusters        = results[2];
      rec.customerClusterHelpers = results[6];
      rec.customerClusters       = rec.customerClusterHelpers[0];
      rec.recommendationMatrix   = rec.customerClusterHelpers[6];
      rec.subClusterHelpers      = results[7].concat(results[8]);
      rec.subClusters            = [];
      for(i = 0; i < rec.subClusterHelpers.length; i++){
        rec.subClusters.push(rec.subClusterHelpers[i][0]);
      }
      rec.powerClusterHelpers    = results[8];
      rec.powerClusters          = [];
      for(i = 0; i < rec.powerClusterHelpers.length; i++){
        rec.powerClusters.push(rec.powerClusterHelpers[i][0]);
      }
      rec.powerRecMatrix         = results[5];
      rec.results                = [rec.customers, rec.products, rec.history, rec.hasPurchased, rec.customersMap, rec.productsMap,
                                    rec.productClusters, rec.customerClusterHelpers, rec.customerClusters, rec.recommendationMatrix,
                                    rec.subClusterHelpers, rec.subClusters, rec.powerClusterHelpers, rec.powerClusters, rec.powerRecMatrix];

      args = Array.prototype.slice.call(arguments,4);
      cb.apply(this,args);
    });
  },

  getRecVariables: function(key){
    if(rec[key] === undefined){
      throw new Error('not a valid recommendation variable');
    } else if(rec[key === null]){
      throw new Error('variable is null.  please run setRecVariables');
    } else{
      return rec[key];
    }
  },

  getRecKeys: function(){
    return Object.keys(rec);
  }
};
