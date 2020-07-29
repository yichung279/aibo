<template lang='pug'>
#app.flex-container.content-center
  .flex-item.flex-container.flex-vertical.margin
    .flex-item.flex-container
      .ui.left.icon.input.inner-margin
        input(type='text', placeholder='Author...', v-model='poster')
        i.users.icon
      .ui.action.labeled.input.inner-margin
        input(type='text', placeholder='Type here...', v-model='url')
        button.left.ui.button(@click='addUrl') Add url
    .ui.list.large
      .ui.label(v-for='(url, index) in addedUrls') {{ url.slice(0, 30) + '...' }}
        i.delete.icon(@click='removeAddedUrl(index)')
    div
      button.primary.ui.button(@click='upload') Upload
    table.ui.celled.table
      thead
        tr
          th URL
          th Collected time
          th Checked time
          th Published time
          th Poster
      tbody
        tr(v-for="(value, index) in news", :class="{ positive: value.checked }")
          td
            .ui.checkbox
              input(type='checkbox', :value='value.url', v-model='selectedNews', @click.stop, :disabled='!auditor')
              label
                a(:href='value.url', @click.stop, target='_blank') {{ value.url }}
          td {{ value.collect_time }}
          td {{ value.checked_time }}
          td {{ value.published_time }}
          td
            .ui.label {{ value.poster }}
    .flex-item
      button.primary.ui.button(@click='checkNews', v-if='auditor') Check
      button.ui.button(@click='deleteNews', v-if='auditor') Delete
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'

const origins = 'https://merry.ee.ncku.edu.tw:1092'
export default {
  async mounted() {
    this.$vlf.getItem('author').then(value => {
      if (value) this.poster = value
    })

    this.getNews()
  },

  data(){return{
    auditor: window.location.href.match(/.*?auditor/),
    poster: '',
    url: '',
    addedUrls: [],
    news: [],
    selectedNews: []
  }},

  methods:{
    addUrl(){
      this.addedUrls.push(this.url)
      this.url = ''
    },

    async getNews(){
      let resopnse = await axios.get(`${origins}/news/30`)
      const news = resopnse.data
      this.news = []
      news.forEach((value, i) => {
        this.$set(this.news, i, value)
      })
    },

    deleteNews(event, index){
      axios.post(`${origins}/deleteNews/`, this.selectedNews)
      const vthis = this
	  Swal.fire({
        title: 'News\' have been deleted',
		icon: 'success',
        showConfirmButton: false,
        timer: 900,
        onAfterClose: function(){
          vthis.getNews()
          vthis.selectedNews = []
        }
	  })
    },

    removeAddedUrl(index){
      this.addedUrls.splice(index, 1)
    },

    checkNews(){
      axios.post(`${origins}/checkNews/`, this.selectedNews)
      const vthis = this
	  Swal.fire({
        title: 'News\' have been checked',
		icon: 'success',
        showConfirmButton: false,
        timer: 900,
        onAfterClose: function(){
          vthis.getNews()
          vthis.selectedNews = []
        }
	  })
    },

    upload(){
      if(this.poster == '') this.poster = 'anonymous'
      axios.post(`${origins}/news/`, {
        "poster": this.poster,
        "urls": this.addedUrls
      })
      const vthis = this
	  Swal.fire({
        title: 'News\' have been saved',
		icon: 'success',
        showConfirmButton: false,
        timer: 900,
        onAfterClose: function(){
          vthis.$vlf.setItem('author', vthis.poster).catch(err => {
            console.log(err)
          })
          vthis.addedUrls = []
          vthis.getNews()
        }
	  })
    },
  }
}
</script>

<style lang="sass">
a
  display: block
  width: 200px
  white-space: nowrap
  text-overflow: ellipsis
  overflow: hidden

.content-center
  justify-content: center

.flex-container
  display: flex

.flex-vertical
  flex-direction: column

.inner-margin
  margin: 0.3rem

.margin
  margin: 3rem

</style>
