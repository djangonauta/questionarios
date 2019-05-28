const router = new VueRouter({
  routes: [
    {path: '/', component: Vue.component('index')},
    {path: '/cadastrar-questionarios', component: Vue.component('questionarios')}
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
