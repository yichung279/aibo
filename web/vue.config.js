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
    messages:{
      entry: 'src/messages/main.js',
      template: 'public/index.html',
      filename: 'messages.html',
      title: 'Messages Page',
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
