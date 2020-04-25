<template>
  <div id="app">
    <div class="left">
      <span
        :class="tagIndex == index ? 'selected' : ''"
        v-for="(name, index) in tags"
        :key="index"
        @click="changeIndex(index)"
      >{{ name }}</span>
    </div>
    <div class="right file-right">
      <div>
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
          <!-- <section id="current-folder"></section>
          <input type="search" id="search" results="3" placeholder="Search" />-->
        </header>
        <!-- 显示文件主区域 -->
        <section id="main-area"></section>
      </div>
    </div>
  </div>
</template>
<script>
const { remote } = require("electron");
const { Menu, MenuItem, Notification } = remote;

import "../assets/css/app.css";
const fs = require("fs");
const fse = require("fs-extra");
const path = require("path");
const mineType = require("mime-types"); // 文件类型
const folderPath = "/Users/houyaohui/Desktop/imgs";

// 文件管理
const fileSystem = require("../../main/fileSystem.js");
const userInterface = require("../../main/userInterface.js");
const search = require("../../main/search.js");
let root,
  resultUrl = [];
export default {
  data() {
    return {
      tagIndex: 5,
      tags: ["图片管理", "视频管理","音乐","其他", "文件管理", "恢复"],
      imgArr: [],
      videoArr: [],
      tag2: false
    };
  },
  mounted() {
    this.main();
  },
  methods: {
    main() {
      const folderPath1 = fileSystem.getUserHomeFolder();

      userInterface.default.setBtnHandler(1);
      userInterface.default.loadDirectory(folderPath1 + "/tmp/");
      userInterface.default.bindSearchField(event => {
        const query = event.target.value;
        if (query === "") {
          userInterface.default.resetFileter();
        } else {
          search.find(query, userInterface.default.filterResults);
        }
      });
    },
    showHint(title, body) {
      let myNotification = new Notification({
        title: title,
        body: body
      });

      myNotification.show();
    },
    changeIndex(index) {
      if (index == this.tags.length-1) {
        return;
      }
      this.$router.push({ path: "/", query: { id: index } });
    },
    open(link) {
      this.$electron.shell.openItem(link);
    }
  }
};
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
}
.file-right{
  padding: 20px 20px 20px 0;
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
