const fs = require('fs')

module.exports = {
  publicPath: '/static',

  pages: {
    oracle:{
      entry: 'src/oracle/main.js',
      template: 'public/index.html',
      filename: 'oracle.html',
      title: 'Oracle Page',
    },
    news:{
      entry: 'src/news/main.js',
      template: 'public/index.html',
      filename: 'news.html',
      title: 'News Page',
    },
    checkedNews:{
      entry: 'src/checkedNews/main.js',
      template: 'public/index.html',
      filename: 'checkedNews.html',
      title: 'checkedNews Page',
    },
  },

  devServer: {
    host: 'merry.ee.ncku.edu.tw',
    port: 1094,
    https: {
      key: fs.readFileSync('/home/yichung/ssl/private.key'),
      cert: fs.readFileSync('/home/yichung/ssl/certificate.crt'),
    },
  },

}
