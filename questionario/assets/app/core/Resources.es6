window.User = {
  install(Vue, options) {
    const url = '/api/v1/usuarios/'
    Vue.prototype.User = Vue.prototype.Resource(url)
  }
}
