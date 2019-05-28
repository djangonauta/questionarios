const app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  filters: {
    pretty: function(value) {
      return JSON.stringify(JSON.parse(value), null, 2);
    }
  },
  data () {
    return {
      questionario: {questoes: []},
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
      ]
    }
  },
  watch: {
    questao (val) {
      console.log(this.questao.tipo_questao)
    }
  },
  methods: {
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
    }
  }
})
