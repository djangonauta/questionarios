Vue.use(bootstrapVue)
Vue.use(Resource)
Vue.use(User)
Vue.use(Questionario)
Vue.use(RespostaQuestao)

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
