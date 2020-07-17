<template lang='pug'>
#app.flex-container.content-center
  .flex-item.flex-container.flex-vertical.margin
    .ui.left.icon.input
      input(type='text', placeholder='user name...', v-model='message')
      i.users.icon
    .ui.action.input
      input(type='text', placeholder='Type here...', v-model='message')
      button.ui.button(@click='boardcast') Add url
    .ui.button(@click='publish()') Publish
</template>

<script>
import axios from 'axios'

export default {
  async mounted() {
    // let resopnse = await axios.get('/urls/')
    // console.log(resopnse.data)
    // this.urls=resopnse.data
    this.urls=['facebook.com', 'amazon.com', 'netflix.com', 'google.com']
  },

  data(){return{
    urls: [],
    checkedUrls: []
  }},

  methods:{
    async publish(){
      await axios.post('/messages/', this.checkedUrls)
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
.flex-horizental
  flex-direction: row
.margin
  margin: 3rem
.input
  margin: 1rem

</style>
