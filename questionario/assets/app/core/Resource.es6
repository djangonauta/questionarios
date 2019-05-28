window.Resource = {
  install(Vue, options) {
    Vue.prototype.Resource = (url, actions) => {
      return Object.assign({
        get: id => axios.get(`${url}${id}/`),
        query: params => axios.get(url, {params}),
        update: obj => axios.put(`${url}${obj.id}/`, obj),
        patch: (obj, params) => axios.patch(`${url}${obj.id}/`, params),
        save: obj => axios.post(url, obj),
        delete: obj => axios.delete(`${url}${obj.id}/`)
      }, actions)
    }
  }
}
