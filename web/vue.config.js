module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:8000/',
        changeOrigin: true
      },
      '^/admin': {
        target: 'http://localhost:8000/',
        changeOrigin: true
      },
      '^/static': {
        target: 'http://localhost:8000/',
        changeOrigin: true
      },
      '^/ws': {
        target: 'ws://localhost:8000/',
        ws: true,
        changeOrigin: true
      }
    }
  }
}
