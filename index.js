
var rec = {};
rec.results              = null;
rec.customers            = null;
rec.products             = null;
rec.purchaseHist         = null;
rec.customersMap         = null;
rec.unfilteredSilhouette = null;
rec.filteredSilhouette   = null;
rec.productClusters      = null;
rec.recommendationMatrix = null;
rec.subClusters          = null;
rec.powerClusters        = null;
rec.unfilteredCluster    = null;

module.exports = Recommender = {
  setRecVariables: function(names, prods, matrix, cb){
    cb = cb || function(){};

    var python = require('child_process').spawn(
      'python',
      ["./pyscript/exec.py", names, prods, matrix]);
    output = '';
    python.stdout.on('data', function(data){
      output += data;
    });
    python.stdout.on('close', function(){
      results = JSON.parse(output);
      rec.results              = results;
      rec.customers            = results[0];
      rec.products             = results[9];
      rec.purchaseHist         = results[10];
      rec.customersMap         = results[1];
      rec.productClusters      = results[2];
      rec.unfilteredSilhouette = results[3];
      rec.filteredSilhouette   = results[4];
      rec.recommendationMatrix = results[5];
      rec.subClusters          = results[6] + results[7];
      rec.powerClusters        = results[6];
      rec.unfilteredCluster    = results[8];

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