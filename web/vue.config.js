const fs = require('fs')

module.exports = {
   publicPath: '/static',

  devServer: {
    host: 'merry.ee.ncku.edu.tw',
    port: 1094,
    https: {
      key: fs.readFileSync('/home/yichung/ssl/private.key'),
      cert: fs.readFileSync('/home/yichung/ssl/certificate.crt'),
    },
  },

}
