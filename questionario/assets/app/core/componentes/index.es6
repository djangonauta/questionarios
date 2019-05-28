Vue.component('index', resolve => {
  axios.get('/public/app/core/componentes/index.html').then(response => {
    resolve({
      template: response.data,
      data () {
        return {

        }
      }
    })
  })
})
