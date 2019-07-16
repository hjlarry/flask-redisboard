const glob = require('glob')
const path = require('path')
const webpack = require('webpack')

const resolve = path.resolve.bind(path, __dirname);

const providePlugin = new webpack.ProvidePlugin({
  $: 'jquery',
  jQuery: 'jquery',
  'window.jQuery': 'jquery',
  Popper: 'popper.js',
  'query-string': 'query-string',
});


const config = {
  entry: glob.sync('./flask_redisboard/src/**/*.js').reduce(
    (entries, entry) => Object.assign(entries, { [entry.split('/').splice(-2, 2).join('/').replace('.js', '')]: entry }), {}),

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.scss$/,
        use: [
          "style-loader",
          "css-loader",
          "sass-loader"
        ]
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.(png|woff|woff2|eot|ttf|svg)$/,
        loader: 'url-loader?limit=100000'
      }
    ]
  },

  output: {
    filename: '[name].js',
    path: path.join(__dirname, 'flask_redisboard/static/dist')
  },

  plugins: [providePlugin,],

  resolve: {
    alias: {
      jquery: resolve('node_modules/jquery/dist/jquery.js'),
    },
  },
  performance: {
    // false | "error" | "warning" // 不显示性能提示 | 以错误形式提示 | 以警告...
    hints: "warning",
    // 开发环境设置较大防止警告
    // 根据入口起点的最大体积，控制webpack何时生成性能提示,整数类型,以字节为单位
    maxEntrypointSize: 5000000,
    // 最大单个资源体积，默认250000 (bytes)
    maxAssetSize: 3000000
  }

}

module.exports = config