var RecommendationEngine    = require('./node/engine');
var Analytics = require('./node/analytics');
var RecommendationVariables = require('./node/variables').GetSet;
var helpers   = require('./node/helpers');

var Recommender = {};

helpers._extend(Recommender, RecommendationEngine, Analytics, RecommendationVariables);

module.exports = Recommender;
