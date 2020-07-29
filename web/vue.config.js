const fs = require('fs')

module.exports = {
  publicPath: '/static',

  pages: {
    news:{
      entry: 'src/news/main.js',
      template: 'public/index.html',
      filename: 'news.html',
      title: 'News Page',
    },
    oracle:{
      entry: 'src/oracle/main.js',
      template: 'public/index.html',
      filename: 'oracle.html',
      title: 'Oracle Page',
    },
    shareNews:{
      entry: 'src/shareNews/main.js',
      template: 'public/index.html',
      filename: 'shareNews.html',
      title: 'shareNews Page',
    },
    checkNews:{
      entry: 'src/checkNews/main.js',
      template: 'public/index.html',
      filename: 'checkNews.html',
      title: 'checkNews Page',
    },
  },

  devServer: {
    host: 'merry.ee.ncku.edu.tw',
    port: 1095,
    https: {
      key: fs.readFileSync('/home/yichung/ssl/private.key'),
      cert: fs.readFileSync('/home/yichung/ssl/certificate.crt'),
    },
  },

}
