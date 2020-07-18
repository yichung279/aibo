<template lang='pug'>
#app.flex-container.content-center
  .flex-item.flex-container.flex-vertical.margin
    .flex-item.flex-container
      .ui.left.icon.input.inner-margin
        input(type='text', placeholder='user name...', v-model='poster')
        i.users.icon
      .ui.action.labeled.input.inner-margin
        .ui.label https://
        input(type='text', placeholder='Type here...', v-model='url')
        button.left.ui.button(@click='addUrl') Add url
    .ui.ordered.list.large
      .item(v-for='url in addedUrls') {{ url }}
    button.teal.ui.button(@click='upload') Upload

</template>

<script>
import axios from 'axios'

export default {
  async mounted() {
  },

  data(){return{
    poster: '',
    url: '',
    addedUrls: []
  }},

  methods:{

    addUrl(){
      this.addedUrls.push('https://'+this.url)
      this.url = ''
    },

    upload(){
      if(this.poster == '') this.poster = 'anonymous'
      axios.post('/news/', {
        "poster": this.poster,
        "urls": this.addedUrls
      })
      this.poster = ''
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
.list
  padding: 0 2rem!important
.margin
  margin: 3rem
.inner-margin
  margin: 0.3rem

</style>
