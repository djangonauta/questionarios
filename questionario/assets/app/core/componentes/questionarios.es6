Vue.component('questionarios', resolve => {
  axios.get('/public/app/core/componentes/questionarios.html').then(response => {
    resolve({
      template: response.data,
      delimiters: ['[[', ']]'],
      data () {
        return {
          questionarios: [],
          questionario: {inicio: new Date(), questoes: []},
          questao: {tipo_questao: 1, alternativas: []},
          alternativa: {},
          questionario_options: {
            1: 'Texto Livre',
            2: 'Única Escolha',
            3: 'Múltipla Escolha',
          },
          questoesFields: [
            'index',
            {key: 'titulo', label: 'Título'},
            {key: 'descricao', label: 'Descrição'},
            {key: 'tipo_questao', label: 'Tipo Questão'},
            {key: 'acao', label: 'Ações'},
          ],
          alternativasFields: [
            'index',
            {key: 'titulo', label: 'Título'},
            {key: 'descricao', label: 'Descrição'},
            {key: 'acao', label: 'Ações'},
          ],
          alternativaOptions: {
            1: 'Padrão',
            2: 'Texto',
            3: 'Múltipla Escolha'
          },
          questionarioFields: [
            {key: 'id', label: 'ID'},
            {key: 'titulo', label: 'Título'},
            {key: 'descricao', label: 'Descrição'},
            {key: 'acoes', label: 'Ações'},
          ]
        }
      },
      methods: {
        carregarQuestionarios () {
          this.Questionario.validos().then(response => {
            this.questionarios = response.data
          })
        },  
        adicionarQuestao () {
          this.questionario.questoes.push(this.questao)
          this.questao = {tipo_questao: 1, alternativas: []}
        },
        removerQuestao (index) {
          this.questionario.questoes.splice(index, 1)
        },
        adicionarAlternativa() {
          this.questao.alternativas.push(this.alternativa)
          this.alternativa = {}
        },
        removerAlternativa (index) {
          this.questao.alternativas.splice(index, 1)
        },
        salvarQuestionario () {
          this.Questionario.save(this.questionario).then(response => {
            this.questionario = {inicio: new Date(), questoes: []}
            this.carregarQuestionarios()
          })
        },
        removerQuestionario (questionario) {
          if (confirm('remover?')) {
            this.Questionario.delete(questionario).then(response => {
              return this.carregarQuestionarios()
            })
          }
        }
      },
      mounted () {
        this.carregarQuestionarios()
      }
    })
  })
})
