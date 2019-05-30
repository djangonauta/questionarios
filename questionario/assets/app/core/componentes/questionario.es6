Vue.component('questionario', resolve => {
  axios.get('/public/app/core/componentes/questionario.html').then(response => {
    resolve({
      template: response.data,
      delimiters: ['[[', ']]'],
      data () {
        return {
          questionario: {}
        }
      },
      beforeRouteEnter (to, from, next) {
        next(vm => vm.setQuestionario(to.params.id))
      },
      methods: {
        setQuestionario (id) {
          this.Questionario.get(id).then(response => {
            this.questionario = response.data
          })
        },
        submeterQuestionario () {
          this.RespostaQuestao.submeterQuestionario(this.questionario).then(() => {
            this.$router.push('/cadastrar-questionarios')
          })
        }
      }
    })
  })
})
