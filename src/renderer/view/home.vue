<template>
  <div id="app">
    <div class="left">
      <span
        :class="tagIndex == index ? 'selected' : ''"
        v-for="(name, index) in tags"
        :key="index"
        @click="changeIndex(index)"
        >{{ name }}</span
      >
    </div>
    <div class="right">
      <div v-show="loading" class="load">
        <img
          src="https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1820729029,1582800583&fm=26&gp=0.jpg"
          alt
        />
      </div>
      <ul class="images" v-show="tagIndex == 0">
        <li
          :title="item.path"
          v-for="(item, index) in imgArr"
          :key="index"
          @mousedown="openMenu(item)"
        >
          <figure v-if="item.suffix.indexOf('image') >= 0">
            <img :src="item.base64Url" />
          </figure>
          <figure v-else>
            <img v-if="item.isFile" src="~@/assets/txt.jpeg" alt />
            <img v-else src="~@/assets/file.jpg" alt />
          </figure>
          <p>{{ item.name }}</p>
        </li>
      </ul>
      <ul class="videos" v-show="tagIndex == 1">
        <li
          v-for="(item, index) in videoArr"
          :key="index"
          @mousedown="openMenu(item)"
        >
          <figure>
            <img src="~@/assets/mp4.png" alt />
          </figure>
          <p>{{ item.name }}</p>
        </li>
      </ul>
      <div v-show="tagIndex == 2">
        <header id="toolBar">
          <section class="navBtnContainer">
            <button class="navBtn" id="backward" disabled>
              <img src="~@/assets/backward.png" alt />
            </button>
            <button class="navBtn" id="forward" disabled>
              <img src="~@/assets/forward.png" alt />
            </button>
            <!-- <button class="navBtn" id="home">
              <img src="~@/assets/home.png" alt />
            </button>-->
          </section>
          <!-- <section id="current-folder"></section> -->
          <!-- <input type="search" id="search" results="3" placeholder="Search" /> -->
        </header>
        <!-- 显示文件主区域 -->
        <section id="main-area"></section>
      </div>
      <ul class="restore" v-show="tagIndex == 3"></ul>
    </div>
  </div>
</template>
<script>
const { remote } = require('electron')
const { Menu, MenuItem, Notification } = remote

import '../assets/css/app.css'
const fs = require('fs')
const fse = require('fs-extra')
const path = require('path')
const mineType = require('mime-types') // 文件类型
const folderPath = '/此电脑/Honor 9i/内部存储/DCIM/Camera'
//

// 文件管理
const fileSystem = require('../../main/fileSystem.js')
const userInterface = require('../../main/userInterface.js')
const search = require('../../main/search.js')
let root,
  resultUrl = []
export default {
  data() {
    return {
      tagIndex: 0,
      tags: ['图片管理', '视频管理', '文件管理', '恢复'],
      imgArr: [],
      videoArr: [],
      tag2: false,
      loading: true
    }
  },
  mounted() {
    if (this.$route.query && this.$route.query.id) {
      this.changeIndex(this.$route.query.id)
    }

    this.$nextTick(() => {
      // setTimeout(() => {
      this.handleReadEvent()
      // }, 600);
    })
    // this.openNodeUsb()
  },
  methods: {
    main() {
      console.log(userInterface.default)

      const folderPath1 = fileSystem.getUserHomeFolder()
      console.log(folderPath1)

      userInterface.default.setBtnHandler()
      userInterface.default.loadDirectory(folderPath1)
      userInterface.default.bindSearchField(event => {
        const query = event.target.value
        if (query === '') {
          userInterface.default.resetFileter()
        } else {
          search.find(query, userInterface.default.filterResults)
        }
      })
    },
    showHint(title, body) {
      let myNotification = new Notification({
        title: title,
        body: body
      })

      myNotification.show()
    },
    // 启动usb监测
    openNodeUsb() {
      console.log('usb')
      var usb = require('usb')

      usb.on('attach', function(device) {
        console.log(device)
      })
    },
    // 桌面
    openMenu(item) {
      const menu = new Menu()
      menu.append(
        new MenuItem({
          label: '备份',
          click: e => {
            // Async with promises:
            fse
              .copy(
                item.path,
                fileSystem.getUserHomeFolder() + '/tmp/' + item.path
              )
              .then(() => {
                this.showHint('提示', '备份成功！')
              })
              .catch(err => console.error(err))
          }
        })
      )
      //
      menu.append(
        new MenuItem({
          label: '查看',
          click: () => {
            this.open(item.path)
          }
        })
      )
      menu.append(
        new MenuItem({
          label: '刷新',
          click: () => {
            this.handleReadEvent()
            setTimeout(() => {
              this.showHint('', '刷新成功')
            }, 600)
          }
        })
      )
      menu.popup({ window: remote.getCurrentWindow() })
    },
    showToast(t) {
      this.hintText = t
      this.hintShow = true
      setTimeout(() => {
        this.hintText = ''
        this.hintShow = false
      }, 3e3)
    },
    changeIndex(index) {
      if (index == 3) {
        // 恢复页面
        this.$router.push('/file')
        return
      }
      this.tagIndex = index
      if (index == 2 && !this.tag2) {
        this.tag2 = true
        this.main()
      }
    },
    open(link) {
      this.$electron.shell.openItem(link)
    },
    handleReadEvent: function() {
      const allUpload = []
      resultUrl = []
      let imgarr = [],
        videoarr = [],
        filearr = []

      try {
        root = fs.readdirSync(folderPath)
        localStorage.setItem('readPath', folderPath)
        let str = ''
        if (root && root.length) {
          root.forEach(m => {
            let postFix = m.split('.')
            let _filetype = 'unknow'
            if (postFix.length > 0) {
              _filetype = postFix[postFix.length - 1]
            }
            const obj = {
              name: m,
              path: folderPath + '/' + m,
              size: 0,
              status: 0,
              date: '',
              isFile: false,
              base64Url: '',
              fileUrl: '',
              type: _filetype,
              suffix: ''
            }
            let imgH = ['bmp', 'jpg', 'jpeg', 'png', 'gif'],
              vidoeH = [
                'mp4',
                'm4v',
                'mov',
                'qt',
                'avi',
                'flv',
                'wmv',
                'asf',
                'mpeg',
                'mpg',
                'vob',
                'mkv',
                'asf',
                'wmv',
                'rm',
                'rmvb',
                'vob',
                'ts',
                'dat'
              ]
            if (imgH.indexOf(_filetype) >= 0) {
              imgarr.push(obj)
            } else if (vidoeH.indexOf(_filetype) >= 0) {
              videoarr.push(obj)
            }

            try {
              const fileInfo = fs.statSync(obj.path)
              const fileType = mineType.lookup(obj.path)
              let data = fs.readFileSync(obj.path)
              data = Buffer.from(data).toString('base64')
              obj.base64Url = 'data:' + fileType + ';base64,' + data
              obj.isFile = fileInfo.isFile()
              obj.suffix = fileType || ''
              obj.size = Math.ceil(fileInfo.size / 1024) + ' KB' || 0

              obj.date =
                new Date(fileInfo.birthtime).format('yyyy-MM-dd hh:mm:ss') || ''

              // 判断是否已经上传
              let localData = localStorage.getItem('recordList')
              localData = localData ? JSON.parse(localData) : []
              const isExist = localData.find(h => h.name == obj.name)
              if (!isExist && obj.isFile && fileType.includes('image')) {
                // 处理
                // allUpload.push({
                //   name: obj.name,
                //   base64Url: obj.base64Url
                // })
                obj.type = 'image'
              } else {
                obj.type = 'file'
                obj.status = 1
                obj.fileUrl = isExist.url
              }
            } catch (error) {}
            // str += `<div class="resultArea_item" path="${folderPath}/${m}">${m}</div>`
          })
          // 排序
          imgarr = this.sortFun(imgarr)
          videoarr = this.sortFun(videoarr)

          // 渲染
          this.imgArr = imgarr
          this.videoArr = videoarr
          this.loading = false
          console.log('渲染', this.imgArr, this.videoArr)
        }
      } catch (error) {
        console.log('错误')
      }
    },
    sortFun(arr) {
      arr.sort(function(a, b) {
        return new Date(b.date).getTime() - new Date(a.date).getTime()
      })
      return arr
    }
  }
}
</script>

<style>
* {
  padding: 0;
  margin: 0;
}
a {
  text-decoration: none;
}
ul,
ol,
li {
  list-style: none;
}
img {
  vertical-align: top;
}
.load {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: #fefefe;
  display: flex;
  justify-content: center;
  align-items: center;
}
.load img {
  width: 300px;
}
#app {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  box-shadow: 0 0 10px 1px #ccc;
  border-radius: 10px;
  background: #f5f5f5;
  display: flex;
}
#app .left {
  width: 200px;
  height: 100%;
  background: #eee;
  box-sizing: border-box;
  flex-shrink: 0;
}
#app .left span,
#app .left a {
  display: block;
  line-height: 40px;
  width: 100%;
  text-align: center;
  border-bottom: 1px solid #ccc;
  background: rgba(0, 0, 0, 0.1);
  color: #fff;
  cursor: pointer;
  font-size: 14px;
}
#app .left span.selected,
#app .left a :hover {
  color: #333;
  background: #fff;
}

.right {
  background: #fff;
  width: 100%;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
  padding: 20px 0 20px 20px;
  position: relative;
}
.right ul {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.right ul li {
  width: 100px;
  margin-bottom: 10px;
  margin-right: 20px;
}
.right ul li figure {
  width: 100%;
  height: 100px;
  /* background: #f5f5f5; */
  line-height: 100px;
  text-align: center;
  overflow: hidden;
}
.right ul li img {
  width: 100%;
  display: block;
  height: 100%;
  object-fit: cover;
}
.right ul li p {
  width: 100px;
  line-height: 28px;
  font-size: 12px;
  color: #333;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  text-align: center;
}
</style>
