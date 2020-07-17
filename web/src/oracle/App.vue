<template lang='pug'>
#app.flex-container.content-center
  .ui.action.input.margin
    input(type='text', placeholder='Type here...', v-model='message')
    button.ui.button(@click='boardcast') Boardcast
</template>

<script>
import axios from 'axios'

export default {
  async mounted() {
  },

  data(){return{
    message: "",
  }},

  methods:{
    async boardcast(){
      await axios.post('/oracle/', this.message)
    }
  }
}
</script>

<style lang="sass">
.flex-container
  display: flex
.content-center
  justify-content: center
.flex-vertical
  flex-direction: column
.margin
  margin: 2rem

</style>
