const router = new VueRouter({
  routes: [
    {path: '/', component: Vue.component('index')},
    {path: '/cadastrar-questionarios', component: Vue.component('questionarios')},
    {name: 'responderQuestionario', path: '/responder/questionario/:id', component: Vue.component('questionario')}
  ]
})

const app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  filters: {
    pretty: function(value) {
      return JSON.stringify(JSON.parse(value), null, 2);
    }
  },
  router
})
