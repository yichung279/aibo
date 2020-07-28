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
      .ui.label(v-for='(url, index) in addedUrls') {{ url }}
        i.delete.icon(@click='deleteUrl(index)')
    button.teal.ui.button(@click='upload') Upload
    table.ui.celled.table
      thead
        tr
          th URL
          th Collected time
          th Checked time
          th Published time
          th Poster
      tbody
        tr(v-for="(value, index) in news", :class="{ checked: value.checked }")
          td
            .ui.checkbox
              input(type='checkbox', :disabled='value.checked', :value='value.url', v-model='checkedNews')
              label
                a(:href='value.url', @click.stop, target='_blank') {{ value.url }}
          td {{ value.collect_time }}
          td {{ value.checked_time }}
          td {{ value.published_time }}
          td
            .ui.label {{ value.poster }}
    .ui.button(@click='publish()', v-if='auditor') Save
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'


export default {
  async mounted() {
    this.getNews()
  },

  data(){return{
    auditor: window.location.href.match(/.*?auditor/),
    poster: '',
    url: '',
    addedUrls: [],
    news: [],
    deletedNews: [],
    checkedNews: [],
  }},

  methods:{
    addUrl(){
      this.addedUrls.push(this.url)
      this.url = ''
    },

    async getNews(){
      let resopnse = await axios.get('https://merry.ee.ncku.edu.tw:1092/news/30')
      const news = resopnse.data
      news.forEach((value, i) => {
        this.$set(this.news, i, value)
      })
    },

    deleteUrl(index){
      this.addedUrls.splice(index, 1)
    },

    publish(){
      axios.post('https://merry.ee.ncku.edu.tw:1092/checkedNews/', this.checkedNews)
      const vthis = this
	  Swal.fire({
		title: 'News\' have been saved',
		icon: 'success',
        onAfterClose: function(){
          vthis.getNews()
        }
	  })
    },

    upload(){
      if(this.poster == '') this.poster = 'anonymous'
      axios.post('https://merry.ee.ncku.edu.tw:1092/news/', {
        "poster": this.poster,
        "urls": this.addedUrls
      })
      const vthis = this
	  Swal.fire({
		title: 'News\' have been saved',
		icon: 'success',
        onAfterClose: function(){
          vthis.addedUrls = []
          vthis.getNews()
        }
	  })
    },
  }
}
</script>

<style lang="sass">
.content-center
  justify-content: center

.flex-container
  display: flex

.flex-vertical
  flex-direction: column

.inner-margin
  margin: 0.3rem

/* .list */
/*   padding: 0 2rem!important */

.margin
  margin: 3rem

tr.checked
  background: #f0ffcc!important

</style>
