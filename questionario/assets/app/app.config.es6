Vue.use(bootstrapVue)
Vue.use(Resource)
Vue.use(User)

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
