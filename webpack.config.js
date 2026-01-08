const path = require('path');

module.exports = {
  mode: 'production',
  entry: './assets/scripts/map.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'paolo_map/static/'),
  },
  module: {
    rules: [
        {
        test: /\.css/i, //regex
        use: [
            'style-loader', //these are external packages
            'css-loader'
            ]
        }
        ]

    }
};