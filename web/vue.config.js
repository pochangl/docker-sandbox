module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://10.2.0.2:8000/',
        changeOrigin: true
      },
      '^/admin': {
        target: 'http://10.2.0.2:8000/',
        changeOrigin: true
      },
      '^/static': {
        target: 'http://10.2.0.2:8000/',
        changeOrigin: true
      },
      '^/ws': {
        target: 'ws://10.2.0.2:8000/',
        ws: true,
        changeOrigin: true
      }
    }
  }
}
