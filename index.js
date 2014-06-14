var rec = {};

rec.results                = null;
rec.customers              = null;
rec.products               = null;
rec.history                = null;
rec.customersMap           = null;
rec.productsMap            = null;
rec.productClusters        = null;
rec.customerClusters       = null;
rec.recommendationMatrix   = null;
rec.customerClusterHelpers = null;
rec.subClusters            = null;
rec.subClusterHelpers      = null;
rec.powerClusters          = null;
rec.powerClustersHelpers    = null;
rec.powerRecMatrix         = null;

module.exports = Recommender = {
  setRecVariables: function(matrix, cb, names, prods){
    names = names || matrix.length;
    prods = prods || matrix[0].length;
    cb = cb || function(){};

    var python = require('child_process').spawn(
      'python',
      [__dirname + '/pyscript/exec.py', names, prods, matrix]);
    output = '';
    python.stdout.on('data', function(data){
      output += data;
    });
    python.stdout.on('close', function(){
      results = JSON.parse(output);
      rec.results                = results;
      rec.customers              = results[0];
      rec.products               = results[4];
      rec.history                = results[11];
      rec.customersMap           = results[1];
      rec.productsMap            = results[3];
      rec.productClusters        = results[2];
      rec.customerClusters       = results[9];
      rec.recommendationMatrix   = results[5];
      rec.customerClusterHelpers = results[8];
      rec.subClusters            = results[9];
      rec.subClusterHelpers      = results[6] + results[7];
      rec.powerClusters          = results[10];
      rec.powerClusterHelpers    = results[6];
      rec.powerRecMatrix         = results[5];

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